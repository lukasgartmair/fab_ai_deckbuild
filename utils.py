#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:17:47 2024

@author: lukasgartmair
"""

import numpy as np


def n_chance(p=0.85):
    if np.random.rand() < p:
        return True
    else:
        print("chance triggered")
        return False


def shift_list(a):
    x = a.pop()
    a.insert(0, x)
    return a
