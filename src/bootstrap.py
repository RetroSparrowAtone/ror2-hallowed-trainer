"""Entry point for the Hallowed Concepts Trainer."""
from __future__ import annotations

import logging
import sys

from src.core.host import TrainerHost
from src.core.contracts import TrainerContext
from src.loader.plugin_loader import PluginLoader
from src.offsets.resolver import OffsetResolver
from src.utils.config import load_config
from src.utils.logger import setup_logging


def main() -> int:
    cfg = load_config("config/local.yaml")
    setup_logging(cfg.trainer.log_level)

    log = logging.getLogger("ror2.trainer")
    log.info("Hallowed Concepts Trainer starting (pid=%s)", __import__("os").getpid())

    resolver = OffsetResolver(cfg.offsets)
    resolver.load()

    ctx = TrainerContext(config=cfg, offsets=resolver, logger=log)
    host = TrainerHost(ctx)
    loader = PluginLoader(host, cfg.plugins)
    loader.discover("src.plugins")
    loader.enable_all()

    try:
        host.run_loop()
    except KeyboardInterrupt:
        log.info("Interrupted, shutting down")
    finally:
        loader.disable_all()
        host.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())