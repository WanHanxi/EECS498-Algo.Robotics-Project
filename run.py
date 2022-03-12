#!/usr/bin/env python
from matplotlib.pyplot import plot
import pybullet as p
import time
from math import pi
import numpy as np
from pybullet_tools.pr2_utils import TOP_HOLDING_LEFT_ARM, PR2_URDF, DRAKE_PR2_URDF, \
    SIDE_HOLDING_LEFT_ARM, PR2_GROUPS, open_arm, get_disabled_collisions, REST_LEFT_ARM, rightarm_from_leftarm
from utils import *
from pybullet_tools.utils import *
from robot import Robot
from particle import Particle
from kalman import Kalman
from path import draw_path, gen_path
from noise import gaussian_noise, gen_noise
from plot import Plot_packet, plot_error
from config import *


def main(kf):
    FILTER: FilterType = FilterType.Kalman
    if kf == 0:
        FILTER = FilterType.Particle

    connect(use_gui=True)
    add_data_path()

    plane = p.loadURDF("plane.urdf")

    robots = {}
    obstacles = {}
    if path_param['type'] == 'eecs':
        robots, obstacles = load_env('map_eecs.json')
    elif path_param['type'] == 'L-turn':
        robots, obstacles = load_env('map_lturn.json')
    obstacles["plane"] = plane
    pr2 = robots["pr2"]
    base_joints = [joint_from_name(pr2, name) for name in PR2_GROUPS['base']]
    p.resetDebugVisualizerCamera( cameraDistance=10, cameraYaw=0, cameraPitch=271, cameraTargetPosition=[13,5,5])
    # set pose to 0 0
    robot = Robot(ground_truth_control_cov)
    kalman = Kalman(filter_param)
    particle = Particle(filter_param)
    set_joint_positions(pr2, base_joints, robot.pose_ground_truth)
    path = gen_path(path_param)
    plot_data: list[Plot_packet] = []
    for index, target in enumerate(path):
        if DEBUG:
            print("ground truth", robot.pose_ground_truth)
            print("sensor: ", robot.pose_sensor)
            print("estimated: ", robot.pose_estimated)
        # calculate control input and update the robot
        target = np.array(target)
        control = target - robot.pose_estimated
        robot.update(control)
        robot.pose_sensor = gen_noise(robot.pose_ground_truth, noise_param)
        if FILTER == FilterType.Kalman:
            robot.pose_estimated = kalman.filter(robot.pose_estimated, control,
                                                 robot.pose_sensor)
        elif FILTER == FilterType.Particle:
            robot.pose_estimated = particle.filter(control, robot.pose_sensor)
        elif FILTER == FilterType.Both:
            robot.pose_estimated = kalman.filter(robot.pose_estimated, control,
                                                 robot.pose_sensor)
            robot.pose_estimated1 = particle.filter(control, robot.pose_sensor)
        # render
        if RENDER_GUI and len(plot_data) > 0:
            draw_line(
                (plot_data[-1].ground_truth[0], plot_data[-1].ground_truth[1],
                 1),
                (robot.pose_ground_truth[0], robot.pose_ground_truth[1], 1),
                PLOT_LINE_WIDTH, (1, 0, 0))
            draw_line((plot_data[-1].estimation1[0],
                       plot_data[-1].estimation1[1], 1),
                      (robot.pose_estimated[0], robot.pose_estimated[1], 1),
                      PLOT_LINE_WIDTH, (0, 0, 1))
            if FILTER == FilterType.Both:
                draw_line(
                    (plot_data[-1].estimation2[0],
                     plot_data[-1].estimation2[1], 1),
                    (robot.pose_estimated1[0], robot.pose_estimated1[1], 1),
                    PLOT_LINE_WIDTH, (0, 1, 0))
            draw_line((path[index - 1][0], path[index - 1][1], 1),
                      (path[index][0], path[index][1], 1), PLOT_LINE_WIDTH,
                      (0, 0, 0))
            # draw_sphere_marker(
            #     (robot.pose_ground_truth[0], robot.pose_ground_truth[1], 1),
            #     0.1, (1, 0, 0, 1))
            # draw_sphere_marker(
            #     (robot.pose_estimated[0], robot.pose_estimated[1], 1), 0.1,
            #     (0, 1, 0, 1))
            # draw_sphere_marker((robot.pose_sensor[0], robot.pose_sensor[1], 1),
            #                    0.1, (0, 0, 1, 1))
            # update robot position in gui
            set_joint_positions(pr2, base_joints, robot.pose_ground_truth)
        # plot prepare
        plot_data.append(
            Plot_packet(robot.pose_ground_truth[:2], robot.pose_sensor[:2],
                        FILTER, robot.pose_estimated[:2],
                        robot.pose_estimated1[:2]))
    if PLOT:
        plot_error(plot_data, FILTER)
    
    # sleep(5000)
    # wait_if_gui('Finish?')
    disconnect()


if __name__ == '__main__':
    main()
