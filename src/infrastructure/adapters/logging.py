import structlog
import logging

logging.basicConfig(
    format="%(message)s",
    level=logging.INFO
)

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()