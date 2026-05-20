import logging

from pythonjsonlogger.jsonlogger import JsonFormatter

from core.context import correlation_id_var


class _CorrelationFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id_var.get()
        return True


def configure_logging() -> None:
    formatter = JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(message)s %(correlation_id)s',
        rename_fields={'asctime': 'timestamp', 'levelname': 'level'},
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(_CorrelationFilter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]
