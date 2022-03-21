#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

def l2p(l):
    return 1 - (1/(1+np.exp(l)))

def p2l(p):
    return np.log(p/(1-p))

def quarternion_to_yaw(qx, qy, qz, qw):
    siny_cosp = 2 * (qw * qz + qx * qy)
    cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
    return np.arctan2(siny_cosp, cosy_cosp)



