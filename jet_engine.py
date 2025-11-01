import os
import sys
import time
import yaml
import numpy as np
import argparse

import IO_funcs
import components_data_fitting
import gas_generator

parser = argparse.ArgumentParser(description="Component matching algorithm for gas generator")
parser.add_argument("--config_file", help="path to configuration file",
                    type=str, default='./config_gas_generator.yaml')#type=str, default='./config_basic_flow_solver.yaml')
parser.add_argument("--res_fldr", help="path to results folder (string ended with /)", type=str, default=None)
config_file = parser.parse_args().config_file

config = IO_funcs.gas_generator_config_reader_yml(config_file, parser)

constants = config.get('constants')
Pamb, Tamb, mach_inlet, R, f = constants['Pamb'], constants['Tamb'], constants['mach_inlet'], constants['R'], constants['f']

gas_generator.gas_generator(config, 10900)


