# -*- coding: utf-8 -*-

'''
Created on 2019��8��19��

@author: admin
'''
import readcig

__version__ = '3.3'
class readconfig(readcig.read_configfile):
    def __init__(self):
        super(readconfig, self).__init__()
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'