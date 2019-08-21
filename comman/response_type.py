# -*- coding: utf-8 -*-
def is_need_res(data):
    request_dic={0:"8001",2:"8106",3:"8107",4:"8201",5:"8202",6:"8900",7:"8103"}
    id=data[2:6]
    for key,value in request_dic.items():
        if value==id:
            return  key
    return 1
