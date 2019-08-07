
import os
from pprint import pprint
import hashlib
import pickle
import time
try:
    from h00_mylittlefunc import tryruntime
except ImportError:
    from .F00_h00 import tryruntime

_='''


# 获得文件的md5码
file_md5(filename)

# 获得路径下文件的信息
path_info(path,T=None,NT=None):

# 如果文件夹不存在则创建文件夹
file_exists_not_create(filename):


# open_write_create_ex 写入str bytes pickle文件 如果路径不存在则创建
def open_wex(filename,data,encoding='utf-8'):

# 读取文件
open_rex

'''

# 获得文件的md5码
def file_md5(filename):
    if not os.path.exists(filename):
        return None
    m2 = hashlib.md5()
    with open(filename,'rb') as f:
        while True:
            data = f.read(1024 * 10)
            if not data:
                break
            m2.update(data)
    return m2.hexdigest()

# 获得路径下文件的信息
def path_info(path,T=None,NT=None):
    path = os.path.normpath(path)
    path = path.replace('\\','/')
    filelst = set()
    for curdir,subdirs,files in os.walk(path):
        for file in files:
            file = os.path.join(curdir,file)
            filelst.add(file[len(path)+1:])

    data = analysis_data(path,filelst,T)
    return data

def analysis_data(basepath,filelst,T=None,NT=None):

    typeset = set()
    fileInfoDict = {}
    for file in filelst:
        type_ = file.split('.')
        if len(type_) > 1:
            type_ = type_[-1]
        else:
            type_ = ' '
        typeset.add(type_)

        if T and type_ not in T:
            continue
        elif NT and type_ in NT:
            continue
        file = file.replace('\\','/')
        fileInfoDict[file] = {'md5':file_md5(os.path.join(basepath,file))}

    return basepath,typeset,fileInfoDict


# 如果文件夹不存在则创建文件夹
def file_exists_not_create(filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

# open_write_ex 写入str bytes pickle(加入了识别头)文件 如果路径不存在则创建
def open_wex(filename,data,encoding='utf-8',ifexists=None,sleep=0):
    isexists = os.path.exists(filename)
    if ifexists:
        if isexists:
            print(filename,end='文件已存在')
            return
    if isexists:
        print(filename,end='文件已被覆盖')

    if callable(data):
        data = data()


    if type(data) == str:
        type_ = 'w'
    elif type(data) == bytes:
        type_ = 'wb'
    else:
        type_ = 'wb'
        data = pickle.dumps(data)
        data = b'<open_wex>' + data

    if type_ == 'wb':
        encoding = None
    elif type_ != 'w':
        raise ValueError('错误的类型参数:%s' % type_)
    try:
        with open(filename,type_,encoding=encoding) as f:
            f.write(data)
    except FileNotFoundError:
        print('create the path')
        os.makedirs(os.path.dirname(filename))
        open_wc(filename,data)
    time.sleep(sleep)
# 读取文件
@tryruntime
def open_rex(filename,type_='r',encoding='utf-8'):
    if type_ == 'rb':
        encoding = None
    with open(filename,'rb') as f:
        data = f.read()
    if data.startswith(b'<open_wex>'):
        data = data[len(b'<open_wex>'):]
        data = pickle.loads(data)
    elif type_ == 'r':
        data = data.decode(encoding)
    return data




if __name__ == '__main__':
    # basepath = r'F:\my\F00_myfn'
    # data = filelst = path_info(basepath,['py'])
    # pprint(data)
    data = '1234 噶'
    filename = 'sdf/asg/fdsg.sdf'
    open_wex(filename,data)
    # filename = 'sdf/asg/fdsg.sdadaff'
    data = open_rex(filename,'rb')
    print(data)