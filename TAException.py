class test_fail(Exception):
    def __init__(self, errmsg, symptom):
        self.errmsg  = errmsg
        self.symptom = symptom
        
class taexception(Exception):
    def __init__(self, exceptiontype, errmsg, symptom):
        # exceptiontype: telnet-1, log-2,config file errror-3,import fail-4,start thread-5,other-6
        self.exceptiontype = exceptiontype 
        self.errmsg          = errmsg
        self.symptom         = symptom
        
class runtime_error(Exception):
    def __init__(self, errmsg):
        self.errmsg  = errmsg