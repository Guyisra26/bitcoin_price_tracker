import uplink
from uplink import get
from models.schemas import SpotPriceResponse
from models.config_schema import CoreDataConfig
from typing import Any

COINBASE_REQUESTS_PER_HOUR_LIMIT = 10000


class CoinbaseAPI(uplink.Consumer):

    def __init__(self, config: CoreDataConfig):
        self._validate_rate_limit(config.run_minutes, config.interval_seconds)
        self.config = config
        super().__init__(base_url=config.base_url)

    @staticmethod
    def _validate_rate_limit(run_minutes: int, interval_seconds: int):
        expected_requests = (run_minutes * 60) // interval_seconds
        if expected_requests > COINBASE_REQUESTS_PER_HOUR_LIMIT:
            raise ValueError(
                f"Requests per hour must be less than {COINBASE_REQUESTS_PER_HOUR_LIMIT}. "
            )

    @get("prices/{base}-{currency}/spot")
    def _fetch_spot_price(self, base: str, currency: str) -> Any:
        """Raw HTTP response for base-currency"""

    def get_price_response(self, base: str, currency: str) -> SpotPriceResponse:
        try:
            raw_response = self._fetch_spot_price(base, currency)
            raw_response.raise_for_status()

            return SpotPriceResponse(**raw_response.json())
        except Exception as e:
            raise ValueError(f"Error fetching spot price from CoinBase: {str(e)}")
