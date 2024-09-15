#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 12:59:36 2024

@author: lukasgartmair
"""

import pygame
import particle
from enum import Enum
import renderer
import animation


class AnimationEndMode(Enum):
    DURATION = 0
    N_TRIGGERS = 1
    CUSTOM = 2


class AnimationQueueType(Enum):
    MAIN = 0
    EVENT = 1


class AnimationQueue:

    def __init__(self, screen):
        self.screen = screen
        self.main_loop_animations = {}
        self.event_queue_animations = {}

    def get_queue(self, animation_queue_type=AnimationQueueType.MAIN):
        if animation_queue_type == AnimationQueueType.MAIN:
            return self.main_loop_animations
        elif animation_queue_type == AnimationQueueType.EVENT:
            return self.event_queue_animations

    def update_animation_queue(self):
        self.main_loop_animations = {
            k: [vi for vi in v if (vi.is_alive == True)]
            for k, v in self.main_loop_animations.items()
            if len([vi for vi in v if vi.is_alive == True]) > 0
        }

        self.event_queue_animations = {
            k: [vi for vi in v if (vi.is_alive == True)]
            for k, v in self.main_loop_animations.items()
            if len([vi for vi in v if vi.is_alive == True]) > 0
        }

    def get_all_animations_of_object(
        self, object_to_be_animated, animation_queue_type=AnimationQueueType.MAIN
    ):
        queue = self.get_queue(animation_queue_type)
        if id(object_to_be_animated) in queue.keys():
            return [a for a in queue[id(object_to_be_animated)]]

    def get_animations_of_certain_type(
        self,
        object_to_be_animated,
        animation_class,
        animation_queue_type=AnimationQueueType.MAIN,
    ):
        queue = self.get_queue(animation_queue_type)

        if id(object_to_be_animated) in queue.keys():
            return [
                a
                for a in queue[id(object_to_be_animated)]
                if isinstance(a, animation_class)
            ]

    def add_to_animation_loop(
        self, animation, animation_queue_type=AnimationQueueType.MAIN
    ):
        queue = self.get_queue(animation_queue_type)

        if id(animation.object_to_be_animated) in queue.keys():
            if animation not in queue:
                queue[id(animation.object_to_be_animated)].append(animation)
            queue[id(animation.object_to_be_animated)].append(animation)
        else:
            queue[id(animation.object_to_be_animated)] = [animation]

    def remove_from_all_queues(self, object_to_be_animated, animation_sequence):
        if id(object_to_be_animated) in list(self.main_loop_animations):
            if (
                animation_sequence
                in self.main_loop_animations[id(object_to_be_animated)]
            ):
                self.main_loop_animations[id(object_to_be_animated)].remove(
                    animation_sequence
                )
        elif id(object_to_be_animated) in list(self.event_queue_animations):
            if (
                animation_sequence
                in self.event_queue_animations[id(object_to_be_animated)]
            ):
                self.event_queue_animations[id(object_to_be_animated)].remove(
                    animation_sequence
                )

    def animate_main_queue(self):

        queue = self.get_queue()
        for k, v in queue.items():
            for vi in v:
                vi.animate()


global animation_queue
animation_queue = AnimationQueue(renderer.Renderer.window)


class BaseAnimation:
    global window

    def __init__(
        self,
        object_to_be_animated=None,
        animation_end_mode=AnimationEndMode.DURATION,
        particle_animation=True,
    ):
        self.screen = renderer.Renderer.window
        self.object_to_be_animated = object_to_be_animated
        print(self.object_to_be_animated)

        self.created_at = pygame.time.get_ticks()

        self.animation_end_mode = animation_end_mode

        self.length_cycle = 1
        self.current_cycle = 0
        self.number_of_cycles = 2

        self.current_time = 0
        self.last_animation_time = 0
        self.triggered = False
        self.first_time_triggered = False

        self.animation_duration = 200
        self.is_alive = True

        self.animation_index = 0

        self.particle_animation = particle_animation
        if self.particle_animation:
            self.particle_system_form = particle.ParticleSystemForm()
            self.particle = particle.Particle(self.particle_system_form)
            self.particle.max_animation_duration = 100

            self.animate_particle_effect = self.animate_particle_effect

    def animate_particle_effect(self):
        self.particle.update()
        self.particle.emit_particles()
        self.particle.render(self.screen.screen_screen)

    def kill(self):
        self.reset()
        self.is_alive = False
        animation_queue.remove_from_all_queues(self.object_to_be_animated, self)

    def custom_kill_function(self):
        pass

    def check_if_should_be_still_is_alive(self):
        if self.animation_end_mode == AnimationEndMode.DURATION:
            if pygame.time.get_ticks() - self.created_at > self.animation_duration:
                # print("stopped for duration")
                self.kill()
        elif self.animation_end_mode == AnimationEndMode.N_TRIGGERS:
            if self.animation_index >= self.number_of_cycles * self.length_cycle:
                # print("stopped for n_triggers")
                self.kill()
        else:
            self.custom_kill_function()

    def initialize_object_to_be_animated(self, object_to_be_animated):
        self.object_to_be_animated = object_to_be_animated

    def animate(self):
        self.check_if_should_be_still_is_alive()
        if self.is_alive:
            self.initialize_object_to_be_animated(self.object_to_be_animated)
        else:
            self.kill()

    def check_animation_trigger(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_animation_time > self.animation_delay:
            self.animation_index += 1
            self.last_animation_time = self.current_time
            self.triggered = True

        else:
            self.triggered = False

    def increase_cycle_counter(self):
        self.current_cycle += 1
        self.animation_index = -1

    def reset(self):
        self.last_animation_time = 0
        self.current_time = 0
        self.animation_index = -1
