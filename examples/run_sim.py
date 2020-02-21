#!/usr/bin/env python3
"""
File:          run_sim.py
Author:        Binit Shah
Last Modified: Binit on 2/20
"""

import argparse
from sim import SimConfig
from agent.block_stacker_pf import BlockStacker
from agent.utilities import Utilities

def main(bin_config_yaml, system_type, auto_enabled_timer):
    c = SimConfig(bin_config_yaml)
    c.auto_enable_timer = auto_enabled_timer
    agent = BlockStacker(Utilities.parse_bin_config(bin_config_yaml), system_type=system_type, sim_config=c)

    while True:
        agent.step()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bin_configuration_yaml", help="file path to the bin configuration yaml", type=str)
    parser.add_argument('-s',
                        default='sim',
                        const='sim',
                        nargs='?',
                        choices=['sim', 'raspi', 'jetson'],
                        help='the hardware system on which this script is running (default: %(default)s)')
    parser.add_argument("--auto_enabled", default=5.0, type=str, help="auto enable timer to test the robot")
    args = parser.parse_args()

    main(args.bin_configuration_yaml, args.s, args.auto_enabled)
