import sys
import os
import time


def find_file_by_head(head,path):
    lst = os.listdir(path)
    for l in lst:
        if l.startswith(head):
            return os.path.join(path,l)


def get_importitems(imports):
    CURRENTURL = os.path.dirname(os.path.dirname(__file__))

    basepath = r'F:\my'

    if not os.path.exists(basepath):
        return

    localpath = os.path.join(CURRENTURL,'gl')

    for im in imports:

        path = find_file_by_head(im[0],basepath)
        if not path: 
            raise ValueError('错误的参数头',im)

        filename = find_file_by_head(im[1],path)

        localfile = os.path.join(localpath,im[0] + '_' + im[1] +'.py')

        with open(filename,'rb') as f:
            data = f.read()

        filename = localfile
        with open(filename,'wb') as f:
            f.write(data)



imports = [
            ('F00','h00'),
            ('F00','h18'),
            ('F00','h17'),
            ]

get_importitems(imports)


from .F00_h00 import tryruntime
from .F00_h17 import reset_window_pos
from .F00_h18 import file_md5,path_info,file_exists_not_create
# from .F00_h13 import request_get

__all__ = ('tryruntime','file_md5',',path_info')