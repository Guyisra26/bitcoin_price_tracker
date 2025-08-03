import time
from datetime import datetime, timedelta
from logging import Logger
from models.schemas import PriceTimeline, SpotPrice
from models.config_schema import CoreDataConfig
from init_services import (
    init_collector,
    init_logger,
    init_email_sender,
    load_config,
    init_grapher,
)


def run_pipeline():
    config = load_config()
    logger = init_logger()

    timeline = run_collector(config.core_config, logger)
    logger.info("Collection complete. check if there is missing data")

    filled_timeline = fill_missing_intervals(
        timeline,
        config.core_config.interval_seconds,
        config.core_config.base,
        config.core_config.currency,
    )
    logger.info("Missing data filled. Generating graph...")
    grapher = init_grapher(logger, config.core_config.base, config.core_config.currency)
    grapher.generate(filled_timeline, interval_time=config.core_config.interval_seconds)
    logger.info("Graph generated. Sending email report...")
    max_price = get_max_price(filled_timeline)
    mailer = init_email_sender(config.email_config, logger)
    mailer.send_report(
        subject=config.email_config.subject,
        body=f"Max price for {config.core_config.base}-{config.core_config.currency} is {max_price}",
        attachment_path=grapher.file_name,
    )


def run_collector(core_config: CoreDataConfig, logger: Logger) -> PriceTimeline:
    collector = init_collector(core_config, logger)
    while not collector.is_complete():
        collector.collect_price(core_config.base, core_config.currency)
        time.sleep(collector.api.config.interval_seconds)

    return collector.storage.load_timeline()


def fill_missing_intervals(
    timeline: PriceTimeline, interval_seconds: int, base: str, currency: str
) -> PriceTimeline:
    if not timeline.prices:
        return timeline

    rounded_prices = {}
    for ts, entry in timeline.prices.items():
        rounded_ts = _round_datetime_to_nearest_interval(ts, interval_seconds)
        if rounded_ts not in rounded_prices:
            rounded_prices[rounded_ts] = entry

    sorted_items = sorted(rounded_prices.items(), key=lambda item: item[0])
    timestamps = [ts for ts, _ in sorted_items]
    values = [entry.amount for _, entry in sorted_items]

    avg = round(sum(values) / len(values), 2)
    filled_prices = {}

    current_time = timestamps[0]
    end_time = timestamps[-1]

    while current_time <= end_time:
        if current_time in rounded_prices:
            filled_prices[current_time] = rounded_prices[current_time]
        else:
            filled_prices[current_time] = SpotPrice(
                pair=f"{base}-{currency}", amount=avg
            )
        current_time += timedelta(seconds=interval_seconds)

    return PriceTimeline(prices=filled_prices)


def _round_datetime_to_nearest_interval(
    dt: datetime, interval_seconds: int
) -> datetime:
    timestamp = dt.timestamp()
    rounded = round(timestamp / interval_seconds) * interval_seconds
    return datetime.fromtimestamp(rounded, tz=dt.tzinfo)


def get_max_price(timeline: PriceTimeline) -> float:
    if not timeline.prices:
        return 0.0
    return max(price.amount for price in timeline.prices.values())
