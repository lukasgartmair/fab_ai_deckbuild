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

np.random.seed(RND_SEED)
random.seed(RND_SEED)

logger = logging.getLogger("root")

if __name__ == "__main__":
    # unittest.main()
    game = Game()

    tb = None

    try:
        game.run(scene_manager.get_title_scene(game.engine, game.renderer))
    except:
        tb = traceback.format_exc()
        print(tb)
        Game.quit_everything()
