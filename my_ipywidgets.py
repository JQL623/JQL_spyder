#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 17:28:37 2020

@author: JQL_2020_4_15
"""
# interact:
#  1. define a function
# 2. call this function
#

import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
from __future__ import print_function

def f(x):
    return x

interact(f,x = 10)

from IPython.display import display

def f(a,b):
    display(a+b)
    return a+b


w = interactive(f(10,20))



