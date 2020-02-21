#!/usr/bin/env python3
"""
File:          utilities.py
Author:        Binit Shah
Last Modified: Binit on 2/21
"""

import yaml

class Utilities:
    """Parser and other useful functions"""

    def parse_bin_config(bin_config_yaml):
        with open(bin_config_yaml, 'r') as stream:
            try:
                ret = yaml.safe_load(stream)
                return [(b['x'], b['y'], b['digit']) for b in ret["blocks"]]
            except yaml.YAMLError as e:
                print(e)
        return []
