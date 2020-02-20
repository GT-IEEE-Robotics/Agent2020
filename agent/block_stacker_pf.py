#!/usr/bin/env python3
"""
File:          block_stacker_pf.py
Author:        Binit Shah
Last Modified: Binit on 2/20
"""

import interface
import planning
import vision
import localization

class BlockStacker:
    """Brain of the block stacker robot"""

    def __init__(self, starting_pose, starting_block_config, system="sim", pose_confidence_threshold=0.95):
        interface.set_system(system)

        self.curr_pose = starting_pose                                      # (x_m, y_m, theta_rad)
        self.remaining_goals = planning.order_blocks(starting_block_config) # [block: (x_m, y_m, color)]
        self.goal = self.blocks_remaining.pop(0)                            # (x_m, y_m, color)
        self.time_left_s = 180.0                                            # 3 minutes
        self.prev_time_s = interface.time()

        self.POSE_CONFIDENCE_THRES = pose_confidence_threshold

    def step(self):
        if not interface.enabled():
            continue

        if planning.reached(self.curr_pose, self.goal):
            self.goal = self.blocks_remaining.pop(0)

        self.curr_pose, confidence = localization.compute_mean_pose()
        if confidence < self.POSE_CONFIDENCE_THRES:
            localization.measurement_update(vision.find_landmarks(interface.read_image()))
            self.curr_pose, confidence = localization.compute_mean_pose()

        omegas = planning.compute_wheel_velocities(self.curr_pose, self.goal)
        interface.command_wheel_velocities(omegas)

        now = interface.time()
        dt = now - self.prev_time_s
        localization.motion_update(interface.read_wheel_velocities(), dt)
        self.time_left_s -= dt
        self.prev_time_s = now
