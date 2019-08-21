# coding=utf-8


import login
import peripheral_polling 
import Binary_Conversion 
import data_compare
import Load_management 
import Oil_management
import Oilwear_management
import Mileage_management
import Temp_management
import Wetness_management
import Reversible_management
import OBD_management
import PSI_management
import Labor_management
import data_processing

__version__ = '3.3'
class application(peripheral_polling.polling,login.login,Binary_Conversion.Binary_conver,data_compare.data_compare,Load_management.load_management,\
                 Oil_management.oil_management,Oilwear_management.oilwear_management,Mileage_management.mileage_management,\
                 Temp_management.temp_management,Wetness_management.wetness_management,Reversible_management.reversible_management,\
                 OBD_management.obd_management,PSI_management.psi_management,Labor_management.labor_management,data_processing.data_processing):
    def __init__(self):
        super(application, self).__init__()
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'