# SPDX-License-Identifier: GPL-3.0-or-later
import logging
import sys
from typing import Literal

import structlog


def configure_logging(transport: Literal["stdio", "http"]) -> None:
    stream = sys.stderr if transport == "stdio" else sys.stdout
    logging.basicConfig(
        level=logging.WARNING,
        stream=stream,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        force=True,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING),
        logger_factory=structlog.PrintLoggerFactory(file=stream),
        cache_logger_on_first_use=True,
    )
