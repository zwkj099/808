# -*- coding: utf-8 -*-
'''
Created on 2019��8��21��

@author: admin
'''
import exrex

#args规则:1-2|^0 如1-2位不能为0
def get_random(*args ):

    #获取长度的开始值、结束值
    if args[0].find('-')!=-1:
        start,end = args[0].split('-')
    else:
        start,end = '',args[0]


    res = ''
    res1=''
    res2=''
    res3=''
    chinesevalue = ''

    #有中文，自动生成最大长度的汉字
    if args[1]=='chinese':
        startpos = 2
        import random
        for k in range(int(end)):
            chinesevalue += unichr(random.randint(0x4e00,0x9fa5))#生成汉字
    else:
        startpos = 1
            
    for i in range(startpos,len(args)):
        if args[i].find('string')!=-1:
            res1 ='a-zA-Z'
        elif args[i].find('int')!=-1:
            res2 ='0-9'
        else:
            res3 += args[i]
    res = res1+res2+res3
    if start !='':

        Forward_data, Forward_data1, Forward_data2, Forward_data3, Forward_boundary_data1, Forward_boundary_data2='','','','','',''
        reverse_boundary_data, reverse_boundary_data1, reverse_boundary_data2 = '','',''

        length='{'+str(int(start)+1)+','+str(int(end)-1)+'}'
        Forward_data = exrex.getone('['+res+']'+length)  # 正向值
        Forward_boundary_data1 = exrex.getone('['+res+']'+'{'+start+'}')#边界正向值
        Forward_boundary_data2 = exrex.getone('['+res+']'+'{'+end+'}')#边界正向值
        if int(start)>1:
            reverse_boundary_data1 = exrex.getone('[' + res + ']' + '{' + str(int(start)-1) +'}')  # 符合其他规则，长度小于边界反向值
        reverse_boundary_data2 = exrex.getone('[' + res + ']' + '{' + str(int(end) + 1) + '}')  # 符合其他规则，长度大于边界反向值
        reverse_data = exrex.getone('[^(' + res + ')]' + '{' + start+','+end + '}')  # 不符合其他规则，长度符合反向值
        if res1!='':
            Forward_data1 = exrex.getone('[' + res1 + ']' + '{' + start + ',' + end + '}')  # 正向值全是字母
        if res2!='':
            Forward_data2 = exrex.getone('[' + res2 + ']' + '{' + start + ',' + end + '}')  # 正向值全是数字
        if res3!='':
            Forward_data3 = exrex.getone('[' + res3 + ']' + '{' + start + ',' + end + '}')  # 正向值全是特殊字符

        Forward_list =[Forward_data, Forward_data1, Forward_data2,Forward_data3,Forward_boundary_data1,Forward_boundary_data2]
        boundary_list =[reverse_data,reverse_boundary_data1,reverse_boundary_data2]

    else:
        length = '{'+end+'}'

        Forward_data, Forward_data1, Forward_data2,Forward_data3='','','',''
        reverse_data, reverse_boundary_data1, reverse_boundary_data2 = '','',''

        Forward_data = exrex.getone('[' + res + ']' + length)  # 正向值
        if res1!='':
            Forward_data1 = exrex.getone('[' + res1 + ']' + length)  # 正向值全是字母
        if res2!='':
            Forward_data2 = exrex.getone('[' + res2 + ']' + length)  # 正向值全是数字
        if res3!='':
            Forward_data3 = exrex.getone('[' + res3 + ']' + length)  # 正向值全是特殊字符

        reverse_data = exrex.getone('[^(' + res + ')]' + length)  # 不符合其他规则，长度符合反向值
        reverse_boundary_data1 = exrex.getone('[' + res + ']' + '{' + str(int(end)-1) +'}')  # 符合其他规则，长度小于边界反向值
        reverse_boundary_data2 = exrex.getone('[' + res + ']' + '{' + str(int(end) + 1) + '}')  # 符合其他规则，长度大于边界反向值
        Forward_list =[Forward_data, Forward_data1, Forward_data2,Forward_data3]
        boundary_list=[ reverse_data, reverse_boundary_data1, reverse_boundary_data2]

    for value in Forward_list:
        if value =='':
            Forward_list.remove(value)
    for value in  boundary_list:
        if value =='':
            boundary_list.remove(value)
    if chinesevalue!='':
        Forward_list.append(chinesevalue)
    
    print chinesevalue

    return [Forward_list, boundary_list]

# if __name__ == '__main__':
#
#     print exrex.getone('[A-Za-z0-9_\-\u4e00-\u9fa5]+')
#
#     #传参规则，前面第1个参数必须为长度，有中文必须在第2个参数填入chinese,没有则可不填
#     """
#     长度传入规则:必须在第一个参数，有范围输入“开始值-结束值”（如2-20）；无开始值，直接输入“结束值”（如20）
#     中文传入规则：必须在第二个参数，写入"chinese"
#     字符串：输入string
#     整数：int
#     其他可以包含的值：直接输入要包含的值
#
#     """
#     a = get_random('2-10','chinese','string','int','_@')
# #     a = get_random('2-20','string','int','_@')
#     # a = get_random('2-20', 'string',)
#     # a = get_random('2-20', 'int',)
#     # a = get_random('2-20',  '_@')
#     # a = get_random('2-20', 'string',  '_@')
#     # a = get_random('2-20', 'int', '_@')
#     print "正向值(长度在中间的值，全是字母，全是数字，全是特殊字符，左边界值，右边界值,中文)+反向值(长度符合其他" \
#           "不符合，其他符合长度小于边界，其他符合长度大于边界)：\n"
#     print a
