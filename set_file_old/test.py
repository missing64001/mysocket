import fileserver
import fileclient
import threading
import socketserver
import time
 


s = input('s/c:')


if s == 's':
    serverIp = '127.0.0.1'
    serverPort = 19821
    serverAddr = (serverIp,serverPort)
     
    class fileServerth(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.create_time = time.time()
            self.local = threading.local()
     
        def run(self):
            print("fileServer is running...")
            fileserver.serve_forever()
     
    fileserver = socketserver.ThreadingTCPServer(serverAddr, fileserver.fileServer)
    fileserverth = fileServerth()
    fileserverth.start()




else:
    serverIp = '127.0.0.1'
    serverPort = 19821
    serverAddr = (serverIp,serverPort)
     
    fileclient = fileclient.fileClient(serverAddr)
    fileclient.sendFile('test.py',r'F:\my')
    fileclient.recvFile('tete.py','/')
