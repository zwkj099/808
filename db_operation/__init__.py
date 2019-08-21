# -*- coding: utf-8 -*-

'''
Created on 2019��8��19��

@author: admin
'''
import interface_db

__version__ = '3.3'
class db_operation(interface_db.interface_db):
    def __init__(self):
        super(db_operation, self).__init__()
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'