#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports
import logging
from rich.logging import RichHandler
from rich.traceback import install
install()


def create_logger():
    """Create a logger for use in all cases."""
    rich_handler = RichHandler(rich_tracebacks=True, markup=True)
    logging.basicConfig(level='INFO', format='%(message)s',
                        datefmt="[%Y/%m/%d %H:%M;%S]",
                        handlers=[rich_handler])
    return logging.getLogger('rich')
