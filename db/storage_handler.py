import json
import os
from datetime import datetime
from logging import Logger
from models.schemas import SpotPrice, PriceTimeline


class StorageHandler:
    def __init__(self, logger: Logger, data_file_name: str = "btc_usd.json"):
        self.file_name = data_file_name
        self.file_path = os.path.join("data", self.file_name)
        self.logger = logger
        os.makedirs("data", exist_ok=True)

    def save_price(self, timestamp: datetime, spot_price: SpotPrice) -> None:
        timeline = self.load_timeline()
        timeline.prices[timestamp] = spot_price

        try:
            with open(self.file_path, "w") as f:
                json.dump(timeline.model_dump(mode="json"), f, indent=2)
                self.logger.info(f"Saved price: {spot_price.amount} at {timestamp}")
        except Exception as e:
            self.logger.error(f"Error saving timeline: {str(e)}")

    def load_timeline(self) -> PriceTimeline:
        if not os.path.exists(self.file_path):
            self.logger.warning(
                f"No data file found at {self.file_path}. Returning empty timeline."
            )
            return PriceTimeline(prices={})
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                return PriceTimeline.model_validate(data)
        except Exception as e:
            self.logger.error(f"Error loading timeline: {str(e)}")
            return PriceTimeline(prices={})

