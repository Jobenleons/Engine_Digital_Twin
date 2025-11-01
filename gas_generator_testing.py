import os
import sys
import time
import yaml
import argparse
import numpy as np
import matplotlib.pyplot as plt

import IO_funcs
from components_data_fitting import compressor_char

parser = argparse.ArgumentParser(description="Component matching algorithm for gas generator")
parser.add_argument("--config_file", help="path to configuration file",
                    type=str, default='./config_gas_generator.yaml')#type=str, default='./config_basic_flow_solver.yaml')
parser.add_argument("--res_fldr", help="path to results folder (string ended with /)", type=str, default=None)
config_file = parser.parse_args().config_file

config = IO_funcs.gas_generator_config_reader_yml(config_file, parser)

constants = config.get('constants')
Pamb, Tamb, mach_inlet, R, f, mc2_bounds = constants['Pamb'], constants['Tamb'], constants['mach_inlet'], constants['R'], constants['f'], constants['mc2_bounds']

component_consts = config.get('compressor')
c2 = component_consts['c2']

nc2_list = np.linspace(500, 10000,100)

plt.figure()


for nc2 in nc2_list:
    mc2_list = np.linspace(1,c2*nc2, 100)
    pr_comp_list = []
    # for 

    for mc2 in mc2_list:
        pr_comp, eff_comp, Tr_c = compressor_char(config,mc2,nc2)
        pr_comp_list.append(pr_comp)

    plt.plot(mc2_list, pr_comp_list)
    
plt.xlabel("mc2")
plt.ylabel("Pr")
plt.title("Compressor map")
plt.show()