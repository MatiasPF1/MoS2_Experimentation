import os 
import time
import numpy as np 
#All Credits to Chuqiao Shi & Chia-hao Lee 20190310
    

                                                # XYZ Parameters
#Inputs By the User
file_name                                      = 0
pixel_size                                     = 0
image_size                                     = 0
metal_atom                                     = 0
chalcogen_atom                                 = 0
lattice_constant_a                             = 0
doped_metal_atom                               = 0
metal_atom_concentration                       = 0
metal_atom_vacancy_concentration               = 0
doped_chalcogen_atom                           = 0
chalcogen_atom_concentration_two_subsititution = 0
chalcogen_atom_concentration_one_subsititution = 0
chalcogen_atom_concentration_one_vacancy       = 0
chalcogen_atom_concentration_two_vacancy       = 0

                                        #Dictionary For Material Parameters
sample_param_dic = {}  
sample_param_dic['file_name'                                     ] = file_name
sample_param_dic['pixel_size'                                    ] = pixel_size
sample_param_dic['image_size'                                    ] = image_size
sample_param_dic['metal_atom'                                    ] = metal_atom
sample_param_dic['chalcogen_atom'                                ] = chalcogen_atom
sample_param_dic['lattice_constant_a'                            ] = lattice_constant_a
sample_param_dic['doped_metal_atom'                              ] = doped_metal_atom
sample_param_dic['metal_atom_concentration'                      ] = metal_atom_concentration
sample_param_dic['metal_atom_vacancy_concentration'              ] = metal_atom_vacancy_concentration
sample_param_dic['doped_chalcogen_atom'                          ] = doped_chalcogen_atom
sample_param_dic['chalcogen_atom_concentration_two_subsititution'] = chalcogen_atom_concentration_two_subsititution
sample_param_dic['chalcogen_atom_concentration_one_subsititution'] = chalcogen_atom_concentration_one_subsititution
sample_param_dic['chalcogen_atom_concentration_one_vacancy'      ] = chalcogen_atom_concentration_one_vacancy
sample_param_dic['chalcogen_atom_concentration_two_vacancy'      ] = chalcogen_atom_concentration_two_vacancy


sample_param_dic['lattice_constant_b'               ] = sample_param_dic['lattice_constant_a']*np.sqrt(3)
sample_param_dic['lattice_constant_c'               ] = 1
sample_param_dic['rep_x'                            ] = int(sample_param_dic['image_size']*sample_param_dic['pixel_size']/sample_param_dic['lattice_constant_a'])
sample_param_dic['rep_y'                            ] = int(sample_param_dic['image_size']*sample_param_dic['pixel_size']/sample_param_dic['lattice_constant_b'])
sample_param_dic['rep_z'                            ] = 1
sample_param_dic['metal_dopant_different'           ] = sample_param_dic['doped_metal_atom'] - sample_param_dic['metal_atom']
sample_param_dic['chalcogen_dopant_different'       ] = sample_param_dic['doped_chalcogen_atom'] - sample_param_dic['chalcogen_atom']
sample_param_dic['dopant_conc_two_subsitutions_high'] = sample_param_dic['chalcogen_atom_concentration_two_subsititution']
sample_param_dic['dopant_conc_one_subsitution_high' ] = sample_param_dic['chalcogen_atom_concentration_one_subsititution']+sample_param_dic['dopant_conc_two_subsitutions_high']
sample_param_dic['dopant_conc_one_vacancy_high'     ] = sample_param_dic['dopant_conc_one_subsitution_high']+sample_param_dic['chalcogen_atom_concentration_one_vacancy']
sample_param_dic['dopant_conc_two_vacancies_high'   ] = sample_param_dic['dopant_conc_one_vacancy_high'] + sample_param_dic['chalcogen_atom_concentration_two_vacancy']
sample_param_dic['supercell_a'                      ] = sample_param_dic['lattice_constant_a'] * sample_param_dic['rep_x']
sample_param_dic['supercell_b'                      ] = sample_param_dic['lattice_constant_b'] * sample_param_dic['rep_y']
sample_param_dic['supercell_c'                      ] = sample_param_dic['lattice_constant_c'] * sample_param_dic['rep_z']
    
                                        #Dictionary For Microscope Parameters
EM_param_dic = {}
voltage                   =   0
Cs3_param_mean            =   0
Cs3_param_std             =   0
Cs5_param_mean            =   0
Cs5_param_std             =   0
df                        =   0
aperture                  =   0
ADF_angle_min             =   0
ADF_angle_max             =   0
Source_size_param_mean    =   0
Source_size_param_std     =   0
defocus_spread_param_mean =   0
defocus_spread_param_std  =   0
probe_current_param_mean  =   0
probe_current_param_std   =   0
dwell_time                =   0



EM_param_dic['voltage']              = voltage
EM_param_dic['Cs3_param']            = (Cs3_param_mean,Cs3_param_std)  
EM_param_dic['Cs5_param']            = (Cs5_param_mean,Cs5_param_std)
EM_param_dic['df']                   = df
EM_param_dic['aperture']             = aperture
EM_param_dic['ADF_angle_min']        = ADF_angle_min
EM_param_dic['ADF_angle_max']        = ADF_angle_max
EM_param_dic["Higher_order"]         = 'END'
EM_param_dic['Source_size_param']    = (Source_size_param_mean, Source_size_param_std)
EM_param_dic['defocus_spread_param'] = (defocus_spread_param_mean,defocus_spread_param_std)
counting_noise                       = 'y'
EM_param_dic['counting_noise']       = counting_noise
EM_param_dic['probe_current_param']  = (probe_current_param_mean,probe_current_param_std)
EM_param_dic['dwell_time']           = dwell_time