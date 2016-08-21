from PyQt5.QtCore import QThread, pyqtSignal
import json

class ResponseThread(QThread):
    
    mySignal = pyqtSignal(str,str)
    
    def __init__(self, socket):
        super().__init__()
        self.socket = socket        
        
    def __del__(self):
        self.wait()

    
    def timeToDuration(self, time):
        duration = time['hours']*3600 + time['minutes']*60 + time['seconds']
        return duration


    def run(self):
        print("Spawning thread")
        while True:
            data = self.socket.recv(1024).decode()
            try:
                d = json.loads(data)
                
                if 'error' in d:
                    print ("Error!")
                    print (d['error'])
                elif 'result' in d:
                    if 'time' in d['result']:
                        param = d['result']
                        totalTime = {
                            'hours' : param['totaltime']['hours'],
                            'minutes' : param['totaltime']['minutes'],
                            'seconds' : param['totaltime']['seconds']
                        }
                        time = {
                            'hours' : param['time']['hours'],
                            'minutes' : param['time']['minutes'],
                            'seconds' : param['time']['seconds']
                        }
                        totTime = self.timeToDuration(totalTime)
                        curTime = self.timeToDuration(time)
                        self.mySignal.emit('time', str(curTime) + '-' + str(totTime))
                    elif 'item' in d['result']:
                        if 'thumbnail' in d['result']['item']:
                            url = str(d['result']['item']['thumbnail'])
                            url = url.split('image://',1)[1]
                            url = url[0:(len(url)-1)]
                            self.mySignal.emit('thumbnail', url)
                        else:
                            print (d['result']['item'])
                    elif 'addons' in d['result']:
                        s=''
                        for addon in d['result']['addons']:
                            s=s+addon['addonid']+'-'
                        self.mySignal.emit('addons', s)
                    else:
                        print (d)
                elif 'method' in d:
                    print ("%s -> %s" % (d['method'],d['params']) )
                    if d['method'] == 'Player.OnPlay':
                        if d['params']['data']['item']['type'] == 'episode':
                            self.mySignal.emit(
                                'play', d['params']['data']['item']['showtitle'] + 
                                ' S' + str(d['params']['data']['item']['season']) +
                                'E' + str(d['params']['data']['item']['episode']) + ' - ' +
                                d['params']['data']['item']['title'] 
                            )
                        else:
                            self.mySignal.emit('play', d['params']['data']['item']['title'])
                    elif d['method'] == 'Playlist.OnAdd':
                        if 'showtitle' in d['params']['data']:
                            self.mySignal.emit('queue', d['params']['data']['item']['showtitle'] + ' - ' + d['params']['data']['item']['title'] )
                    else:
                        self.mySignal.emit(d['method'], 'OK')
                else:
                    print ( d )
            except json.decoder.JSONDecodeError:
                #print (data)
                print ("Error while decoding json")         
