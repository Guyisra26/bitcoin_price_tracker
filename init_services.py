import json
from logging import Logger

from models.config_schema import AppConfig, CoreDataConfig, EmailDataConfig
from client.coinbase_api import CoinbaseAPI
from core.price_collector import PriceCollector
from utils.logger_factory import LoggerFactory
from db.storage_handler import StorageHandler
from handlers.graph_handler import GraphHandler
from handlers.email_handler import EmailSender


def load_config(path: str = "config.json") -> AppConfig:
    with open(path, "r") as f:
        data = json.load(f)
    return AppConfig(**data)


def init_logger() -> Logger:
    return LoggerFactory.create_logger()


def init_email_sender(email_config: EmailDataConfig, logger: Logger) -> EmailSender:
    return EmailSender(config=email_config, logger=logger)


def init_grapher(logger: Logger, base: str, currency: str) -> GraphHandler:
    file_name = f"{base.lower() + '_' + currency.lower() + '_graph'}.png"
    return GraphHandler(logger=logger, file_name=file_name)


def init_storage(
    logger: Logger, base: str = "BTC", currency: str = "USD"
) -> StorageHandler:
    file_name = f"{base.lower() + '_' + currency.lower()}.json"
    return StorageHandler(data_file_name=file_name, logger=logger)


def init_collector(core_config: CoreDataConfig, logger: Logger) -> PriceCollector:
    api = CoinbaseAPI(core_config)
    storage = init_storage(logger, core_config.base, core_config.currency)
    return PriceCollector(api=api, storage_handler=storage, logger=logger)
