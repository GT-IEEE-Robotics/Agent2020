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

    def __init__(self, starting_block_goals, starting_pose=(0, 0, 0), system_type="sim",
                 sim_config=None, pose_confidence_threshold=0.95):
        interface.set_system(system_type, sim_config=sim_config)

        self.curr_pose = starting_pose                                      # (x_m, y_m, theta_rad)
        self.remaining_goals = starting_block_goals                         # [block: (bin_num, offset_m)]
        goal = self.remaining_goals.pop(0)                                  # (bin_num, offset_m)
        planning.queue_bin(self.curr_pose, goal[0], goal[1])
        self.time_left_s = 180.0                                            # 3 minutes
        self.prev_time_s = interface.get_time()

        self.POSE_CONFIDENCE_THRES = pose_confidence_threshold

    def step(self):
        if not interface.is_enabled():
            self.prev_time_s = interface.get_time()
            return

        if planning.wp_done():
            goal = self.remaining_goals.pop(0)
            planning.queue_bin(self.curr_pose, goal[0], goal[1])

        self.curr_pose, confidence = localization.compute_mean_pose()
        if confidence < self.POSE_CONFIDENCE_THRES:
            localization.measurement_update(vision.find_landmarks(vision.ignore_outside(interface.read_image())))
            self.curr_pose, confidence = localization.compute_mean_pose()

        omegas = planning.compute_wheel_velocities(self.curr_pose)
        interface.command_wheel_velocities(omegas)

        now = interface.get_time()
        dt = now - self.prev_time_s
        localization.motion_update(interface.read_wheel_velocities(), dt)
        self.time_left_s -= dt
        self.prev_time_s = now
