import os
import sys
import time
import yaml
import numpy as np
import argparse
import IO_funcs

def diffuser(config):
    constants = config.get('constants')
    Pamb, Tamb, mach_inlet, R, f = constants['Pamb'], constants['Tamb'], constants['mach_inlet'], constants['R'], constants['f']
    component_consts = config.get('diffuser')
    gamma_diff = component_consts['gamma_diff']
    pr_dd = component_consts['pr_dd']
    d = component_consts['d']

    Tt2 = (Tamb*(1+(((gamma_diff-1)/2)*mach_inlet*mach_inlet)))
#     Tt2

    ua = mach_inlet*np.sqrt(gamma_diff*R*Tamb*1000)

    pr_d = pr_dd*(1-d*((mach_inlet+1)**(1.35)))

    Pt2 =  Pamb*pr_d*(1+(((gamma_diff-1)/2)*mach_inlet*mach_inlet))**(gamma_diff/(gamma_diff-1))
    return Tt2,Pt2

def compressor_char(config,mc2,nc2):
    component_consts = config.get('compressor')
    c1 = component_consts['c1']
    c2 = component_consts['c2']
    c3 = component_consts['c3']
    c4 = component_consts['c4']
    c5 = component_consts['c5']
    u = component_consts['u']
    eff_c_dp = component_consts['eff_c_dp']
    nc2d = component_consts['nc2d']
    gamma_comp = component_consts['gamma_comp']

    pr_comp =1 + c1*mc2*np.sqrt(abs(((mc2/(c2*nc2))-1)/(c3 -1)))
       
    c6 = c3*(u+1)
    mc2d = c6*c2*nc2
    eff_comp=eff_c_dp-(c4*abs(nc2d-nc2))-(((c5/nc2)*(mc2d-mc2)**2))

    Tr_c=((pr_comp**((gamma_comp-1)/gamma_comp)-1)/eff_comp)+1
    return pr_comp, eff_comp, Tr_c

def combustor(config, mc3, Tt3):
    constants = config.get('constants')
    Pamb, Tamb, mach_inlet, R, f = constants['Pamb'], constants['Tamb'], constants['mach_inlet'], constants['R'], constants['f']
    component_consts = config.get('combustor')
    b1 = component_consts['b1']
    b2 = component_consts['b2']
    delta_h = component_consts['delta_h']
    eff_burner_dp = component_consts['eff_burner_dp']
    gamma_b = component_consts['gamma_b']

    pr_b=1-((b1*mc3**2)*(f/(Tt3/Tamb))**2)
    cp=(gamma_b*R)/(gamma_b-1)
    Tr_b=(f*eff_burner_dp*delta_h+(cp*Tt3))/((cp*Tt3)*(1+f))
    return pr_b, Tr_b

def turbine(config, mc4,nc4):
    component_consts = config.get('turbine')
    k1, k2 = component_consts['k1'], component_consts['k2']
    mc4c = component_consts['mc4c']
    nc4d = component_consts['nc4d']
    pr_tc = component_consts['pr_tc']
    eff_t_d = component_consts['eff_t_d']
    
    c_par = mc4/mc4c
    n_par = nc4/(2*nc4d)
    if c_par>1:
#         print(mc4,nc4)
        x_par = 1
        pr_t_inverse = ((x_par**(1/n_par))*((1/pr_tc)-1))+1  #first prt found
        
    else:
        x_par = 1 - np.sqrt(1-c_par)
        pr_t_inverse = ((x_par**(1/n_par))*((1/pr_tc)-1))+1  #first prt found
    
    pr_t = 1/pr_t_inverse
    eff_t = eff_t_d*(1-(k1*((((1/pr_t)-(1/pr_tc))/((1/pr_tc)-1))**2))-k2*(((mc4c*nc4d-mc4*nc4)/(mc4c*nc4d))**2))
#     eff_t = eff_t_d*(1-(k1*((((1/pr_t)-(1/pr_tc))/((1/pr_tc)-1))**2))-k2*(((mc4c*nc4d-mc4*nc4)/(mc4c*nc4d))**2))
    return pr_t,eff_t