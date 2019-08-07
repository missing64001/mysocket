#!/usr/bin/python3

import sys,os
from socket import *
from select import *
try:
    from gl.gl import tryruntime,file_md5,path_info,reset_window_pos,file_exists_not_create
except ImportError:
    from .gl import tryruntime,file_md5,path_info,reset_window_pos,file_exists_not_create
import time
from pprint import pprint
import pickle

FILEIOSIZE = 40

import re


def main():
    title='mysocket--server'
    N = reset_window_pos(title)





    if N:
        s = 'c'
        os.system('title mysocket--client')
    else:
        os.system('title %s' % title)
        s = 's'

    MyS = SynchroData() # '120.79.41.9'

    if s == 's':
        MyS.server()
    elif s == 'c':
        MyS.clientfile = r'F:\tmp'
        MyS.serverfile = r'F:\tmpserver'
        MyS.client()
        MyS.synchro_download(MyS.soc)
        # MyS.synchro_upload(MyS.soc)
    else:
        print('启动时输入了错误的参数')

            
class SynchroData(object):

    client_d = {}
    isfiletrans = False

    def __init__(self,host='localhost'):
        self.host = host
        self.port = 9999
        self.soc = socket(AF_INET,SOCK_STREAM)
        self.isclient = None
        # self._homepath = '/home/tarena/桌面/h_recv/'
        # print('判断是否有文件夹,并创建')
    def server(self):
        print('开启了服务器')
        self.soc.setsockopt(SOL_SOCKET,SO_REUSEADDR,True)
        self.soc.bind(('0.0.0.0',self.port))
        self.soc.listen(10)


        rlst = [self.soc]
        wlst = []
        xlst = []

        while True:
            rs,ws,xs = select(rlst,wlst,xlst,1)
            for r in rs:
                if r == self.soc:
                    conn,addr = self.soc.accept()
                    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),addr,"连接服务器")
                    self.__class__.client_d[conn] = [addr]
                    rlst.append(conn)
                elif r in self.__class__.client_d:
                    try:
                        data = r.recv(1024*FILEIOSIZE)
                        if not data:
                            raise ConnectionResetError('')

                        da = re.findall(r'code:sendfilestart<([\w\W]+?)><([\w\W]+?)>',data.decode('utf-8'))
                        if len(da) == 1:
                            da = da[0]
                            type_ = da[0]
                            da = da[1]
                            if type_ == 'send_file':
                                self.send_file(r,da)
                            elif type_ == 'send_file':
                                self.recv_file(r,da)
                        elif data == b'synchro_download':
                            r.send(b'get_synchro_download')
                            self.serverfile = r.recv(1024*FILEIOSIZE).decode('utf-8')
                            self.synchro_upload(r)

                        elif data == b'synchro_upload':
                            self.synchro_download(r)
                        else:
                            print(11,data.decode('utf-8'))
                    except ConnectionResetError:
                        print(self.__class__.client_d[r],'断开了连接')
                        self.__class__.client_d.pop(r)
                        rlst.remove(r)
                        r.close()

                else:
                    print('进行了错误的连接')


            for w in ws:
                pass

            for x in xs:
                pass

        
    def client(self):
        print('开启了客户端')
        self.isclient = True
        # ,sys.stdin
        self.soc.connect((self.host,self.port))
        self.soc.settimeout(10)
        rlst = [self.soc]
        wlst = []
        xlst = []
        

    def send_file(self,soc,path):
        md5 = file_md5(path)
        if not md5:
            print('文件不存在')
            return
        size = os.path.getsize(path)
        info = '<path=%s><size=%s><md5=%s>' % (path,size,md5)
        soc.send(info.encode('utf-8'))

        data = soc.recv(1024*FILEIOSIZE)
        if data == b'code:ok':
            print(path,'开始发送文件',end='\r')
        elif data == b'code:wrong':
            print('验证码错误')
        else:
            raise ValueError(data.decode('utf-8'))


        with open(path,'rb') as f:
            while True:
                data = f.read(1024*FILEIOSIZE)
                if not data:
                    break
                soc.send(data)
        info = '<endpath=%s><size=%s><md5=%s>' % (path,size,md5)
        soc.send(info.encode('utf-8'))

        data = soc.recv(1024*FILEIOSIZE)
        if data == b'code:sendfileend':
            print(path,'传输完成    ')
            soc.send(b'xx')
        elif data == b'code:sendfilewrong':
            print(path,'文件传输出现错误')
            soc.send(b'xx')
        else:
            print('获得了错误的代码 1', data)

    def recv_file(self,soc,path,savepath=None):
        if not savepath:
            savepath = path
        soc.send(b'code:sendfilestart<send_file><%s>' % path.encode('utf-8'))
        data = soc.recv(1024*FILEIOSIZE)
        da = re.findall(r'<path=([\w\W]+?)><size=(\d+)><md5=([\w\W]+?)>',data.decode('utf-8'))
        if len(da) == 1:
            da = da[0]
            soc.send(b'code:ok')



            path, size, md5 = da



            file_exists_not_create(savepath)
            with open(savepath,'wb') as f:
                while True:
                    data = soc.recv(1024*FILEIOSIZE)
                    if data.endswith(('<endpath=%s><size=%s><md5=%s>' % (path, size, md5)).encode('utf-8')):
                        f.write(data[:-len(('<endpath=%s><size=%s><md5=%s>' % (path, size, md5)).encode('utf-8'))])
                        break
                    elif data == 'exit()':
                        return
                    f.write(data)


            fmd5 = file_md5(savepath)

            if fmd5 == md5:
                soc.send(b'code:sendfileend')
                soc.recv(1024*FILEIOSIZE)
                print(savepath,'传输完成    ')
            else:
                soc.send(b'code:sendfilewrong')
                soc.recv(1024*FILEIOSIZE)
                print(fmd5,md5)
                print(path,'文件传输失败')
        else:
            print(data)
            soc.send(b'code:wrong')
            raise ValueError('错误的参数1')

    def synchro_upload(self,soc):
        if self.isclient:
            soc.send(b'synchro_upload')
            if soc.recv(1024*FILEIOSIZE) != b'get_synchro_upload':
                raise ValueError('错误的参数，应该是%s' % 'get_synchro_upload')

            soc.send(self.serverfile.encode('utf-8'))
            data = soc.recv(1024*FILEIOSIZE)
            if data != b'get_serverfile':
                raise ValueError('错误的参数，应该是%s' % 'get_serverfile')
            uploadfile = self.clientfile
        else:
            uploadfile = self.serverfile


        pinfo = path_info(uploadfile,[' '])
        pinfo = pickle.dumps(pinfo)
        print('pinfo',len(pinfo))
        soc.send(pinfo)
        soc.send(b'<pinfo_end>')

        if self.isclient:
            while True:
                data = soc.recv(1024*FILEIOSIZE)
                if data == b'code:sendfileend':
                    break
                da = re.findall(r'code:sendfilestart<([\w\W]+?)><([\w\W]+?)>',data.decode('utf-8'))
                da = da[0][1]
                self.send_file(soc,da)

    def synchro_download(self,soc):
        if self.isclient:
            soc.send(b'synchro_download')
            
            data = soc.recv(1024*FILEIOSIZE)
            if data != b'get_synchro_download':
                raise ValueError('错误的参数，应该是%s' % data.decode('utf-8'))

            basepath = self.clientfile
            updownfile = self.serverfile
            soc.send(updownfile.encode('utf-8'))
        else:
            soc.send(b'get_synchro_upload')
            basepath = soc.recv(1024*FILEIOSIZE).decode('utf-8')
            soc.send(b'get_serverfile')

        data = b''
        while True:
            data += soc.recv(1024*FILEIOSIZE)
            if data.endswith(b'<pinfo_end>'):
                data = data[:-len(b'<pinfo_end>')]
                break
        data = pickle.loads(data)
        
        sData = data[2]
        server_basepath = data[0]
        cData = path_info(basepath,[' '])[2]
        for filename,md5 in sData.items():
            if cData.get(filename) != md5:
                print(filename,'开始发送',end='\r')
                self.recv_file(soc,server_basepath+'/'+filename,basepath+'/'+filename)

        for filename,md5 in cData.items():
            if filename not in sData:
                if input('删除文件%s,请输入(y):' % filename) == 'y':
                    os.remove(os.path.join(basepath,filename))

        if not self.isclient:
            soc.send(b'code:sendfileend')

    def __exit__(self,a=None,b=None,c=None):
        self.soc.close()
if __name__ == '__main__':
    main()




