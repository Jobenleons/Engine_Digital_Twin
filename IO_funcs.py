import os
import sys
import time
import yaml
import numpy
import argparse

def gas_generator_config_reader_yml(input_file_path, parser):
    if input_file_path.endswith('yaml'):
        with open(input_file_path, "r") as configfile:
            configs = yaml.load(configfile, yaml.SafeLoader)
    else:
        config_format = os.path.splitext(input_file_path)[1]
        raise Exception("unknown input file format: " + config_format)

    if hasattr(parser.parse_args(), 'res_fldr'):
        if parser.parse_args().res_fldr is not None:
            configs['output']['res_fldr'] = parser.parse_args().res_fldr
    
    # comm = MPI.comm_world
    # rank = comm.Get_rank()
    # if rank==0:
    if not os.path.exists(configs['output']['res_fldr']):
        os.makedirs(configs['output']['res_fldr'])
    with open(configs['output']['res_fldr']+'settings.yaml', 'w') as outfile:
        yaml.dump(configs, outfile, default_flow_style=False)
    
    return configs