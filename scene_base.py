#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:10:50 2023

@author: lukasgartmair
"""


class SceneBase:
    def __init__(
        self,
        engine=None,
        renderer=None,
    ):
        self.next = self
        self.engine = engine
        self.renderer = renderer
        self.is_active = True

        self.render()

        # for k, v in self.sprite_groups.items():
        #     setattr(self, k, v)

    def process_input(self):
        print("uh-oh, you didn't override this in the child class")

    def get_scene_data(self):
        print("uh-oh, you didn't override this in the child class")

    def update(self):
        print("uh-oh, you didn't override this in the child class")

    def render(self):
        print("uh-oh, you didn't override this in the child class")

    def switch_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.switch_to_scene(None)
        self.is_active = False
