from PyQt5.QtCore import QThread, pyqtSignal
import json

class ResponseThread(QThread):
    
    mySignal = pyqtSignal(str,str)
    
    def __init__(self, socket):
        super().__init__()
        self.socket = socket        
        
    def __del__(self):
        self.wait()
        
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
                        self.mySignal.emit('time', json.dumps(d['result']))
                    elif 'item' in d['result']:
                        if 'thumbnail' in d['result']['item']:
                            d2 = d['result']['item']['thumbnail']
                            self.mySignal.emit('thumbnail', str(d2))
                        else:
                            print (d['result']['item'])
                    else:
                        print (d)
                elif 'method' in d:
                    print ("%s -> %s" % (d['method'],d['params']) )
                    if d['method'] == 'Player.OnPlay':
                        if d['params']['data']['item']['type'] == 'episode':
                            self.mySignal.emit(
                                d['method'], d['params']['data']['item']['showtitle'] + 
                                ' S' + str(d['params']['data']['item']['season']) +
                                'E' + str(d['params']['data']['item']['episode']) + ' - ' +
                                d['params']['data']['item']['title'] 
                            )
                        else:
                            self.mySignal.emit(d['method'], d['params']['data']['item']['title'])
                    elif d['method'] == 'Playlist.OnAdd':
                        self.mySignal.emit(d['method'], d['params']['data']['item']['showtitle'] + ' - ' + d['params']['data']['item']['title'] )
                    else:
                        self.mySignal.emit(d['method'], 'OK')
                else:
                    print ( d )
            except json.decoder.JSONDecodeError:
                #print (data)
                print ("Error while decoding json")         
