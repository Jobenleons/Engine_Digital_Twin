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
                    type=str, default='./config_gas_generator.yaml')
parser.add_argument("--res_fldr", help="path to results folder (string ended with /)", type=str, default=None)
config_file = parser.parse_args().config_file

config = IO_funcs.gas_generator_config_reader_yml(config_file, parser)
constants = config.get('constants')
component_consts = config.get('compressor')
c2 = component_consts['c2']

nc2_list = np.linspace(500, 30000, 100)
num_mc2_points = 100
mc2_mat = np.zeros((len(nc2_list), num_mc2_points))
pr_mat = np.zeros_like(mc2_mat)
eff_mat = np.zeros_like(mc2_mat)

plt.figure(figsize=(10,7))

for i, nc2 in enumerate(nc2_list):
    mc2_list = np.linspace(1, c2 * nc2, num_mc2_points)
    mc2_mat[i, :] = mc2_list
    pr_list = []
    for j, mc2 in enumerate(mc2_list):
        pr_comp, eff_comp, Tr_c = compressor_char(config, mc2, nc2)
        pr_list.append(pr_comp)
        pr_mat[i, j] = pr_comp
        if eff_comp>0:
            eff_mat[i, j] = eff_comp
        else:
            eff_mat[i, j] = 0
    plt.plot(mc2_list, pr_list)


contour_lines = plt.contour(mc2_mat, pr_mat, eff_mat, levels=20, colors='k', linestyles='dashed')
plt.clabel(contour_lines, inline=True, fontsize=8)  # Label contour lines
plt.xlabel("mc2")
plt.ylabel("Pr")
plt.title("Compressor Efficiency Contour Map")
plt.savefig('compressor_map.png', dpi=300, bbox_inches='tight')
plt.show()