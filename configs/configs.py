#coding=utf-8

import os
import sys
#Env Settings
#ROOT_PATH='/Users/imiyoo/workplace/tscanner'

#获取当前配置文件的绝对路径
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
LIB_PATH	= ROOT_PATH + '/thirdparty/'

#加载关键路径
sys.path.append(ROOT_PATH)
sys.path.append(LIB_PATH)

#File&Path Settings
DOMAIN_FILE 	= ROOT_PATH + ''
DIR_HOST_FILE   = ROOT_PATH + ''
DIR_WEB_FILE    = ROOT_PATH + ''
FINGER_FILE     = ROOT_PATH + ''

#Env Path Settings
TEYE_PY_PATH    = ROOT_PATH + ''
NMAP_PATH       =''
PYTHON_ENV      =''

#SqlHelper Settings
class Configuration:
    SQLALCHEMY_DATABASE_URI = ''

class DevelopmentConfiguration(Configuration):
    pass

class ProductConfiguration(Configuration):
    pass


_config_table = {
        'default': DevelopmentConfiguration,
        'develope': DevelopmentConfiguration,
        'product': ProductConfiguration,
        }


#Database Settings
WAT_Host='X.X.X.X'        #database host info
WAT_Database='wat'        #database name info
WAT_User='root'           #database user info
WAT_Pass='root'           #database pass info

#Activemq Settings
ACTIVEMQ_ADDRESS="tcp://X.X.X.X:61617"
ACTIVEMQ_IP='X.X.X.X'
ACTIVEMQ_PORT='61617'
ACTIVEMQ_WATSERVER_QUEUE='/queue/WATSERVER'
ACTIVEMQ_WATCLIENT_QUEUE='/queue/WATCLIENT'
ACTIVEMQ_WATAPP_QUEUE='/queue/WATAPP'
ACTIVEMQ_USER='system'
ACTIVEMQ_PASSWORD='manager'


#Rpc Settings
RPYC_HOST="X.X.X.X"
RPYC_PORT=8888


#Dispatch Settings
MSG_INTERVAL=1
BIG_MSG_INTERVAL=1*60
RECV_MSG_TIME_IDLE =30
MAX_SCAN_TIME = 2*60*60
MAX_CONCURRENT_NUM = 2
MAX_DISPATCH_TASK = 10
MAX_RETRY_COUNT = 5
RETRY_INTERVAL = 1
SCAN_TASK_INTERVAL = 60
DISPATCH_TASK_INTERVAL= 10


#COMMON VULNS
SQL_KB=""
XSS_KB=""
LFI_KB=""
CMD_KB=""
BAK_KB=""


H=u'高危'
M=u'中危'
L=u'低危'
N=u'提示'
