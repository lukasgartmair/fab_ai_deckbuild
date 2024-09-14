#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 12:59:36 2024

@author: lukasgartmair
"""

import pygame
import particle
from enum import Enum
import animation


class AnimationEndMode(Enum):
    DURATION = 0
    N_TRIGGERS = 1
    CUSTOM = 2


class AnimationQueueType(Enum):
    MAIN = 0
    EVENT = 1


class AnimationQueue:

    global window

    def __init__(self):
        self.main_loop_animations = {}
        self.event_queue_animations = {}

    def get_queue(self, animation_queue_type=AnimationQueueType.MAIN):
        if animation_queue_type == AnimationQueueType.MAIN:
            return self.main_loop_animations
        elif animation_queue_type == AnimationQueueType.EVENT:
            return self.event_queue_animations

    def update_animation_queue(self):
        self.main_loop_animations = {
            k: v for k, v in self.main_loop_animations.items() if v
        }
        self.event_queue_animations = {
            k: v for k, v in self.event_queue_animations.items() if v
        }

    def get_all_animations_of_object(
        self, animation_object, animation_queue_type=AnimationQueueType.MAIN
    ):
        queue = self.get_queue(animation_queue_type)
        if id(animation_object) in queue.keys():
            return [a for a in queue[id(animation_object)]]

    def get_animations_of_certain_type(
        self,
        animation_object,
        animation_class,
        animation_queue_type=AnimationQueueType.MAIN,
    ):
        queue = self.get_queue(animation_queue_type)

        if id(animation_object) in queue.keys():
            return [
                a for a in queue[id(animation_object)] if isinstance(a, animation_class)
            ]

    def add_to_animation_loop(
        self, animation_object, animation, animation_queue_type=AnimationQueueType.MAIN
    ):
        queue = self.get_queue(animation_queue_type)

        if id(animation_object) in queue.keys():
            if animation not in queue:
                queue[id(animation_object)].append(animation)
            queue[id(animation_object)].append(animation)
        else:
            queue[id(animation_object)] = [animation]

    def remove_from_all_queues(self, animation_object, animation_sequence):
        if id(animation_object) in list(self.main_loop_animations):
            if animation_sequence in self.main_loop_animations[id(animation_object)]:
                self.main_loop_animations[id(animation_object)].remove(
                    animation_sequence
                )
        elif id(animation_object) in list(self.event_queue_animations):
            if animation_sequence in self.event_queue_animations[id(animation_object)]:
                self.event_queue_animations[id(animation_object)].remove(
                    animation_sequence
                )

    def animate_main_queue(self):

        queue = self.get_queue()
        for k, v in queue.items():
            v.animate(v)


class BaseAnimation:
    global window

    def __init__(
        self,
        animation_end_mode=AnimationEndMode.DURATION,
        particle_animation=True,
    ):
        self.camera = window
        self.animation_object = None

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
        self.particle.render(self.camera.camera_screen)

    def kill(self):
        self.reset()
        self.is_alive = False
        animation.animation_queue.remove_from_all_queues(self.animation_object, self)

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

    def initialize_animation_object(self, animation_object):
        self.animation_object = animation_object

    def animate(self, animation_object):
        self.check_if_should_be_still_is_alive()
        if self.is_alive:
            self.initialize_animation_object(animation_object)
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
