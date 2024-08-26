#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 17:12:18 2024

@author: lukasgartmair
"""

import logging


def setup_custom_logger(name):
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)
    logger.addHandler(handler)
    return logger


logger = setup_custom_logger("root")
