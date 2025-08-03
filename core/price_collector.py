from datetime import datetime
from client.coinbase_api import CoinbaseAPI
from db.storage_handler import StorageHandler
from models.schemas import SpotPrice
from logging import Logger


class PriceCollector:
    def __init__(
        self, api: CoinbaseAPI, storage_handler: StorageHandler, logger: Logger = None
    ):
        self.api = api
        self.storage = storage_handler
        self.logger = logger
        self.collected = 0
        self.target_iterations = self.compute_max_iterations(
            self.api.config.run_minutes, self.api.config.interval_seconds
        )

    def collect_price(self, base: str, currency: str) -> bool:
        timestamp = datetime.now()
        try:
            response = self.api.get_price_response(base, currency)
            spot_price = SpotPrice(
                pair=f"{base}-{currency}", amount=float(response.data.amount)
            )
        except Exception as e:
            spot_price = None
            self.logger.warning(f"Failed to fetch price from API: {str(e)}")

        self.collected += 1

        if spot_price is None:
            return False

        self.storage.save_price(timestamp=timestamp, spot_price=spot_price)
        self.logger.info(f"Price saved (entry #{self.collected}) at {timestamp}")
        return True

    @staticmethod
    def compute_max_iterations(run_minutes: int, interval_seconds: int) -> int:
        return (run_minutes * 60) // interval_seconds

    def is_complete(self) -> bool:
        return self.collected >= self.target_iterations
