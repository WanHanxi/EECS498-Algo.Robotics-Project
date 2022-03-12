#!/usr/bin/env python
from math import pi, cos, sin
from utils import draw_sphere_marker
import numpy as np


def draw_path(path: list, radius=0.1, color=(0, 0, 0, 1)) -> None:
    for pt in path:
        draw_sphere_marker((pt[0], pt[1], 1), radius, color)


def gen_path(param: dict) -> list:
    if param['type'] == 'circle':
        return gen_path_circle(param['radius'], param['step'])
    if param['type'] == 'L-turn':
        return gen_path_lturn(param['step'])
    if param['type'] == 'eecs':
        return gen_path_eecs(param['step'])


def gen_path_circle(r: float, step: float) -> list:
    angle = 0
    path = []
    while angle < 2 * pi:
        path.append((r * sin(angle), -r * cos(angle) + r, angle))
        angle += step
    return path


def move(x: float, y: float, angle: float, dx: float, dy: float, dangle: float,
         step: float) -> list:
    path = []
    while dx != 0 or dy != 0 or dangle != 0:
        path.append((x, y, angle))
        if abs(dx) < step:
            x += dx
            dx = 0
        elif abs(dx) == dx:
            x += step
            dx -= step
        else:
            x -= step
            dx += step

        if abs(dy) < step:
            y += dy
            dy = 0
        elif abs(dy) == dy:
            y += step
            dy -= step
        else:
            y -= step
            dy += step

        if abs(dangle) < step:
            angle += dangle
            dangle = 0
        elif abs(dangle) == dangle:
            angle += pi / 4
            dangle -= pi / 4
        else:
            angle -= pi / 4
            dangle += pi / 4

    path.append(np.array([x, y, angle]))
    return path


def gen_path_lturn(step: float) -> list:
    x = 0
    y = 0
    angle = 0
    path = []

    #move +x
    path.extend(move(x, y, angle, 13, 0, 0, step))
    x += 13

    #turn
    path.extend(move(x, y, angle, 0, 0, pi / 2, step))
    angle += pi / 2

    #move +y
    path.extend(move(x, y, angle, 0, 13, 0, step))
    y += 13

    return path


def gen_path_eecs(step: float) -> list:
    x = 0
    y = 0
    angle = 0
    path = []

    #move x+7
    path.extend(move(x, y, angle, 7, 0, 0, step))
    x += 7

    #turn +pi/2
    path.extend(move(x, y, angle, 0, 0, pi / 2, step))
    angle += pi / 2

    #move y+3
    path.extend(move(x, y, angle, 0, 3, 0, step))
    y += 3

    #move x-3
    path.extend(move(x, y, angle, -3, 0, 0, step))
    x -= 3

    #move y+1
    path.extend(move(x, y, angle, 0, 1, 0, step))
    y += 1

    #move x+3
    path.extend(move(x, y, angle, 3, 0, 0, step))
    x += 3

    #move y+7
    path.extend(move(x, y, angle, 0, 7, 0, step))
    y += 7

    #turn -pi/2
    path.extend(move(x, y, angle, 0, 0, -pi / 2, step))
    angle -= pi / 2

    #move x+12
    path.extend(move(x, y, angle, 12, 0, 0, step))
    x += 12

    #turn -pi/2
    path.extend(move(x, y, angle, 0, 0, -pi / 2, step))
    angle -= pi / 2

    #move y-3
    path.extend(move(x, y, angle, 0, -3, 0, step))
    y -= 3

    #move x-3, y-3
    path.extend(move(x, y, angle, -3, -3, 0, step))
    x -= 3
    y -= 3

    #move x+3, y-3
    path.extend(move(x, y, angle, 3, -3, 0, step))
    x += 3
    y -= 3

    #move y-2
    path.extend(move(x, y, angle, 0, -2, 0, step))
    y -= 2

    #turn +pi/2
    path.extend(move(x, y, angle, 0, 0, pi / 2, step))
    angle += pi / 2

    #move x+7
    path.extend(move(x, y, angle, 7, 0, 0, step))
    x += 7

    return path