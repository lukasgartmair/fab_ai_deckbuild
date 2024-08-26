#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:29:21 2023

@author: lukasgartmair
"""

from game import Game
import numpy as np
import random
import logging
from settings import RND_SEED
import scene_manager
import traceback
import asyncio

np.random.seed(RND_SEED)
random.seed(RND_SEED)

logger = logging.getLogger("root")


web = False


def main_local():
    game = Game()

    tb = None

    try:
        game.run(scene_manager.get_title_scene(game.engine, game.renderer))
    except:
        tb = traceback.format_exc()
        print(tb)
        Game.quit_everything()


async def main_web():
    game = Game()
    running = True
    tb = None

    while running:
        try:
            game.run(scene_manager.get_title_scene(game.engine, game.renderer))

        except:
            tb = traceback.format_exc()
            print(tb)
            Game.quit_everything()
        await asyncio.sleep(0)


if __name__ == "__main__":
    if web:
        asyncio.run(main_web())

    else:
        main_local()
