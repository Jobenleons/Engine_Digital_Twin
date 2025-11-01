import os
import sys
import time
import yaml
import numpy as np
import argparse

from scipy.optimize import minimize_scalar

import IO_funcs
import components_data_fitting



def required_turbine_pressure(config, n_true, Tr_b, Tr_c, Tt4, eff_t):
    therm_consts = config.get('thermodynamics')
    gamma_m1 = therm_consts['gamma_m1']
    gamma_m2 = therm_consts['gamma_m2']

    shaft_consts = config.get('shaft')
    s1 = shaft_consts['s1']
    s2 = shaft_consts['s2']

    constants = config.get('constants')
    Pamb, Tamb, mach_inlet, R, f = constants['Pamb'], constants['Tamb'], constants['mach_inlet'], constants['R'], constants['f']

    eff_mech = 1-s1*n_true**s2

    cp1 = (gamma_m1*R)/(gamma_m1-1)
    cp2 = (gamma_m2*R)/(gamma_m2-1)
    Tr_t = 1-((cp1*(Tr_c - 1)/((eff_mech*(1+f)*cp2*Tr_b*Tr_c))))
    
    Tt5 = Tr_t * Tt4
    gamma5=1.328
    PR_t=(1+ ((Tr_t-1)/eff_t))**(gamma5/(gamma5-1))
    
    return PR_t

def error_prt(config, mc2, nc2):
    constants = config.get('constants')

    Pamb, Tamb, mach_inlet, R, f = constants['Pamb'], constants['Tamb'], constants['mach_inlet'], constants['R'], constants['f']

    Tt2,Pt2 = components_data_fitting.diffuser(config)
    
    n_true = nc2*(np.sqrt(Tt2/Tamb))

    pr_comp, eff_comp, Tr_c = components_data_fitting.compressor_char(config, mc2, nc2)

    Tt3=Tr_c*Tt2
    
    mc3=mc2*np.sqrt(Tr_c)/pr_comp

    pr_b, Tr_b = components_data_fitting.combustor(config, mc3, Tt3)

    Tt4=Tr_b*Tt3
    mc4=(mc2*(f+1)*np.sqrt(Tr_b*Tr_c)/(pr_b*pr_comp))
    nc4 = nc2/np.sqrt(Tr_b*Tr_c)

    pr_t,eff_t = components_data_fitting.turbine(config, mc4,nc4)

    PR_t = required_turbine_pressure(config, n_true, Tr_b, Tr_c, Tt4, eff_t)

    error_p = abs(PR_t-pr_t)*100/pr_t

    return error_p

def gas_generator(config, nc2, mc2_bounds = [50,100]):
    
    result = minimize_scalar(lambda mc2: error_prt(config, mc2, nc2),bounds = mc2_bounds, tol=0.0001)

    if result.success:
        best_mc2 = result.x
        lowest_error = result.fun
        print(f"Best mc2: {best_mc2}, Lowest error: {lowest_error}")
    else:
        print("Minimization failed:", result.message)