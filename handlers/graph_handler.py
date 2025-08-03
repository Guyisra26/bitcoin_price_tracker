import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from models.schemas import PriceTimeline
from logging import Logger


class GraphHandler:
    def __init__(self, logger: Logger, file_name: str = "btc_usd_graph.png"):
        self.file_name = file_name
        self.logger = logger

    def generate(self, timeline: PriceTimeline, interval_time: int = 60) -> None:
        if not timeline.prices:
            self.logger.warning("No data available to plot.")
            return
        timestamps = list(timeline.prices.keys())
        prices = [entry.amount for entry in timeline.prices.values()]
        currency = timeline.prices[next(iter(timeline.prices))].pair

        try:
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, prices, marker="o", linestyle="-", linewidth=2)
            plt.title(f"{currency} - Bitcoin Price Index (BPI)")
            plt.xlabel("Time")
            plt.ylabel("Price (USD)")
            plt.grid(True)
            ax = plt.gca()
            ax.xaxis.set_major_locator(mdates.SecondLocator(interval=interval_time))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            plt.gcf().autofmt_xdate()
            plt.tight_layout()
            plt.savefig(self.file_name)
            plt.close()

            self.logger.info(f"Graph saved to {self.file_name}")
        except Exception as e:
            self.logger.error(f"Failed to generate graph: {e}")
