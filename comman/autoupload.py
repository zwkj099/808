#coding=utf-8
import xlrd

def readexcel():
    file_path = r'./comman/upload.xlsx'
    workbook = xlrd.open_workbook(file_path)
    data_sheet = workbook.sheets()[0]
    row_num = data_sheet.nrows
    col_num = data_sheet.ncols

    list = []
    for i in range(2,row_num):
        rowlist = []
        for j in range(col_num):
            rowlist.append(data_sheet.cell_value(i,j))
        list.append(rowlist)
    return  list
