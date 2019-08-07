from h01_synchrodata import SynchroData


while True:
    try:
        MyS = SynchroData('120.79.41.9') #

        MyS.clientfile = r'F:\my\P040_exchange_api'
        MyS.serverfile = r'/home/uftp/my/download_history'
        # MyS.serverfile = r'D:\my\P040_exchange_api'
        MyS.client()

        MyS.synchro_download(MyS.soc)
        # MyS.synchro_upload(MyS.soc)
    except Exception as e:
        raise e
        MyS.soc.send(b'exit()')
        MyS.soc.close()
        print('出错重启')
        print(e)
    else:
        break

