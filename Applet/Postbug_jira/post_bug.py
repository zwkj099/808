#encoding:utf8
"""
function:自动上传bug至jira
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import requests
from db_operation.mysql_connect import Mysql


def postbug(username,password,project,status,issueid=0,priority='',assignee='',summary='',description='',components='',customfield='',customfield_10303=''):
    """
    :param username:用户名
    :param password:登录密码
    :param project:项目名称
    :param status:状态 0：新增 1：待观察 2：重启 3：关闭 4：延后  5：拒绝
    :param issueid:bug编号 如LYXJ-789
    :param priority:优先级 1：紧急 2：高 3：中 4：一般 5：低  10000：N/A
    :param assignee:经办人 请参考jira_user.csv文件
    :param summary:概要
    :param description:描述
    :param components:模块
    :param customfield:bug分类  需求类、功能类、前端界面类、性能类、安全类、接口、易用性、安装部署/配置类
    :param customfield_10303:严重程度  致命、严重、一般、轻微
    :return:
    """
    ############################################################
    ############获取登录后的cookie##############################
    ############################################################

    #登录时需要POST的数据
    data = {'os_username':username,
     'os_password':password}

    #登录时表单提交到的地址（用开发者工具可以看到）
    login_url = 'http://192.168.24.250:8080/login.jsp'

    #构造Session
    session = requests.Session()
    resp = session.get(login_url)
    cookie = resp.cookies
    # print cookie    #登录前cookie

    resp = session.post(login_url, data)
    # print resp.cookies     #成功登录后的cookie
    # print resp.status_code
    formToken = resp.cookies.items()[0][1]
    atl_token = resp.cookies.items()[1][1]

    ############################################################
    ############判断传入的属性在数据库是否存在##################
    ############################################################

    # 打开数据库连接
    mysql_test = Mysql('192.168.24.250','3306','root','Zwkj@123Mysql','jira',charset='utf8')

    #"customfield_10107"
    customfielddict = {"需求类":"10034","功能类":"10003","前端界面类":"10004","易用性":"10006","性能类":"10007",\
                       "安全类":"10200","安装部署/配置类":"10203","接口":"10008"}
    # customfieldid ='-1'#无

    #customfield_10303 严重程度
    customfield_10303dict = {"致命":"10101","严重":"10102","一般":"10103","轻微":"10104"}
    # customfield_10303id = '-1' #无

    if status ==0 or status ==6:#如果是新增或者修改
        try:
            if customfield!='':
                customfieldid = customfielddict[customfield]
        except Exception as e:
            print e
            print "传入的bug分类错误"

        try:
            if customfield!='':
                customfield_10303id = customfield_10303dict[customfield_10303]
        except Exception as e:
            print e
            print "传入的严重程度错误"

    # print customfieldid
    # print customfield_10303id
    #查询平台的项目
    projectdic = {}
    sql = "select DISTINCT object_id,object_name from audit_item where object_type='PROJECT'"
    result = mysql_test.query(sql)
    for res in result:
        projectdic[res[1].decode('utf-8')]=res[0]

    #读取参数
    status = status
    project = project
    try:
        projectid = projectdic[project.decode('utf-8')]  # 10500 林业巡检id
    except Exception as e:
        print e
        print "传入的项目名称错误"

    componentid = '-1'
    if status == 0 or status == 6:  # 如果是新增或者修改
        #查询此项目有哪些模块
        componentdict = {}
        sql = "select * from component where project ="+str(projectid)
        result = mysql_test.query(sql)
        for res in result:
            componentdict[res[2].decode('utf-8')]=res[0]
        try:
            componentid =  componentdict[components.decode('utf-8')]#获取传进来的模块id
        except Exception as e:
            print e
            print "传入的模块错误"

    issuenum =0
    id = ''
    issuestatus=''
    if issueid!=0 and status!=0:
        issuenum = issueid.split('-')[1]
        # 获取bugid
        sql = "select * from jiraissue where issuenum="+issuenum+" and project="+projectid
        result = mysql_test.query(sql)
        id = str(result[0][0])
        issuestatus = str(result[0][13])



    ############################################################
    ############根据传入的类型，执行对应的操作##################
    ############################################################

    if status==0 and issueid==0:#新增

        #设置请求头

        headers = {
            "Host": "192.168.24.250:8080",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Connection":"keep-alive",
            "Content-Length": "954",
            "charset":"UTF-8",
            "cookie":"JSESSIONID="+formToken+";"+"atlassian.xsrf.token="+atl_token

        }

        print "JSESSIONID="+formToken+";"+"atlassian.xsrf.token="+atl_token

        data1={
            "pid": projectid, #项目id
            "issuetype": "10100",#问题类型【故障】 需求：10200
            "atl_token":atl_token,
            "formToken": formToken,
            "priority": priority,  #优先级3:【中】  2:高
            "assignee": assignee,#经办人
            "summary": summary,#概要
            "description": description,#描述
            "components": componentid,  #模块id
            "customfield_10107":customfieldid, #bug分类id
            "customfield_10303":customfield_10303id #严重程度
        }
        resp1 = requests.post('http://192.168.24.250:8080/secure/QuickCreateIssue.jspa?decorator=none',\
                            data1,headers=headers)
        print resp1.text
        resultdict =json.loads(resp1.text)
        return resultdict['issueKey']   #返回bugid LYXJ-809

    elif status==1 and issuestatus!='10004':#待观察
        # print "待观察"
        url="http://192.168.24.250:8080/secure/WorkflowUIDispatcher.jspa?id="+id+"&action=81&atl_token="+atl_token
        resp1 = session.get(url)
        return resp1.status_code

    elif status == 2:#重启
        url="http://192.168.24.250:8080/secure/WorkflowUIDispatcher.jspa?id="+id+"&action=41&atl_token="+atl_token
        if issuestatus=='10004':
            url = "http://192.168.24.250:8080/secure/WorkflowUIDispatcher.jspa?id=" + id + "&action=91&atl_token=" + atl_token #延后之后重启
        resp1 = session.get(url)
        return resp1.status_code

    elif status==3:#关闭close
        url="http://192.168.24.250:8080/secure/WorkflowUIDispatcher.jspa?id="+id+"&action=51&atl_token="+atl_token
        resp1 = session.get(url)
        return resp1.status_code

    elif status==4:#延后
        url="http://192.168.24.250:8080/secure/WorkflowUIDispatcher.jspa?id="+id+"&action=71&atl_token="+atl_token
        resp1 = session.get(url)
        return resp1.status_code


    elif status == 5 and issuestatus!='10004':#拒绝
        url="http://192.168.24.250:8080/secure/WorkflowUIDispatcher.jspa?id="+id+"&action=21&atl_token="+atl_token
        resp1 = session.get(url)
        return resp1.status_code

    elif status == 6:#修改
        #设置请求头

        headers = {
            "Host": "192.168.24.250:8080",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Connection":"keep-alive",
            "Content-Length": "954",
            "charset":"UTF-8",
            "cookie":"JSESSIONID="+formToken+";"+"atlassian.xsrf.token="+atl_token

        }

        print "JSESSIONID="+formToken+";"+"atlassian.xsrf.token="+atl_token

        data={
            "id": id, #bug id
            "issuetype": "10100",#问题类型【故障】 需求：10200
            "atl_token":atl_token,
            "formToken": formToken,
            "priority": priority,  #优先级3:【中】  2:高
            "assignee": assignee,#经办人
            "summary": summary,#概要
            "description": description,#描述
            "components": componentid,  #模块id
            "customfield_10107":customfieldid, #bug分类id
            "customfield_10303":customfield_10303id #严重程度
        }
        resp1 = requests.post('http://192.168.24.250:8080/secure/QuickEditIssue.jspa?issueId='+id+'&decorator=none',\
                            data,headers=headers)
        return resp1.status_code

    else:
        print "传参有误"

    mysql_test.close_mysql()

#
# if __name__=='__main__':
#
#     bugid = postbug('yangdanyuan','123456','林业巡检',0,0,priority='3',assignee='yangdanyuan',summary='概要post',description='描述内容',components='监控调度',customfield='前端界面类',customfield_10303='严重')#新增，返回bug编号，如LYXJ-793
#     print bugid
#     status_code = postbug('yangdanyuan','123456','林业巡检', 1, 'LYXJ-786')#待观察       成功200
#     status_code=postbug('yangdanyuan','123456','林业巡检', 2, 'LYXJ-809')#重启
#     status_code=postbug('yangdanyuan','123456','林业巡检', 3, 'LYXJ-793')#关闭
#     status_code=postbug('yangdanyuan','123456','林业巡检', 4, 'LYXJ-793')#延后
#     status_code= postbug('yangdanyuan','123456','林业巡检', 5, 'LYXJ-793')#拒绝
#     status_code=postbug('yangdanyuan','123456','林业巡检',6,'LYXJ-809',priority='3',assignee='ailili',summary='概要post-modify',description='描述内容-modify',components='监控调度',customfield='功能类',customfield_10303='一般')#修改
#
#










