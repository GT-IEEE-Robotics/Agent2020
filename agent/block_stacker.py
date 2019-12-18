#!/usr/bin/env python3
"""
File:          block_stacker.py
Author:        Binit Shah
Last Modified: Binit on 12/17
"""

import time

from pathplanning.planner import plan_next_goal, reached
from vision.vo import process_visual_odometry
from sensor.encoder import process_encoders
from localization.ekf import localize

class BlockStacker:
    """Coordinates all planning and motion
    of the block stacker robot.
    """

    def __init__(self, start_location_m, start_block_layout, path_err_threshold_m=0.1, orient_err_threshold_rad=0.02):
        self.PATH_ERROR_THRES_m = path_err_threshold_m
        self.ORIENT_ERROR_THRES_rad = orient_err_threshold_rad
        self.PATH_FOLLOWING_MODE = 0
        self.ORIENTING_MODE = 1
        self.PICKUP_MODE = 2
        self.FINISHED_MODE = 3

        self.curr_location_m = start_location_m
        self.time_left_s = 180.0 # 3 minutes
        self.blocks_remaining = start_block_layout

        self.goal = None # (block_id, block_location_m)
        self.path = None # List(path_intermediate_location_m)
        self.path_err = 0.0
        self.mode = self.PATH_FOLLOWING_MODE
        self.last_time_s = time.time()

    def path_following_step(self):
        if self.goal == None or self.path == None or self.path_err >= self.PATH_ERROR_THRES_m:
            self.goal, self.path = plan_next_goal(self.curr_location_m, self.time_left_s, self.blocks_remaining, self.goal)

        dpos_dynamics_m, self.path, self.path_err = follow_path(self.curr_location_m, self.path)
        dpos_image_m = process_visual_odometry()
        dpos_sensor_m = process_encoders()

        self.curr_location_m = localize(dpos_dynamics_m, dpos_image_m, dpos_sensor_m)

        if reached(self.curr_location_m, self.goal[1]):
            self.path = None
            self.path_err = 0.0
            self.mode = self.ORIENTING_MODE

    def orienting_step(self):
        if self.goal == None:
            raise TransitionError("Expected to orient to a goal")

        # skip this step
        self.mode = self.PICKUP_MODE

    def pickup_step(self):
        if self.goal == None:
            raise TransitionError("Expected to pickup a goal block")

        # skip this step
        self.blocks_remaining.del(self.goal[0])
        self.goal = None
        self.mode = self.PATH_FOLLOWING_MODE

    def step(self, dt):
        self.time_left_s -= dt
        if self.time_left_s <= 0.0:
            self.mode = self.FINISHED_MODE

        if self.mode == self.PATH_FOLLOWING_MODE:
            self.path_following_step()
        elif self.mode == self.ORIENTING_MODE:
            self.orienting_step()
        elif self.mode == self.PICKUP_MODE:
            self.pickup_step()
        elif self.mode == self.FINISHED_MODE:
            return
