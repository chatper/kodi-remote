import sys, socket, json, urllib.request, argparse
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QDialog, QLabel, QMessageBox, QProgressBar
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, QBasicTimer
from ResponseThread import ResponseThread
from HelpWidget import HelpWidget

class Gui(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.mySocket = socket.socket()
        self.params = {}
        self.responseThread = ResponseThread(self.mySocket)
        self.isPlaying = False
        
        self.setGeometry(300, 300, 420, 420)
        self.setWindowTitle('Kodi Remote Control')
        self.setWindowIcon(QIcon('./img/icon.png'))
        
        self.img = QLabel('img', self)
        self.img.setGeometry((420-256)/2,(380-256)/2,256,256)
        self.img.setPixmap(QPixmap('./img/splash.png'))
        
        self.status = QLabel('OK', self)
        self.status.setGeometry(0,380,400,20)
        
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(0,400,410,20)
        self.progress = 0
        
        self.timer = QBasicTimer()
        
        self.show()
        
        self.responseThread.mySignal.connect(self.handleSignals)
        self.responseThread.start()
        

    def handleSignals(self, signal, param):
        #print("Signal caught")
        if signal == 'Input.OnInputRequested':
            self.showInputDialog()
            print("Text sending")
        if signal == 'Player.OnStop':
            self.isPlaying = False
            self.status.setText( 'Nothing playing now' )
            self.img.setPixmap(QPixmap('./img/splash.png'))
            if self.timer.isActive():
                self.timer.stop()
                self.pbar.setValue(0)
                print('Stoping timer')
        if signal == 'Player.OnPlay':
            self.isPlaying = True
            self.status.setText( param )
            self.rpc("Player.GetItem",{"properties":["thumbnail","fanart"],"playerid":1}, True)
            if not self.timer.isActive():
                self.timer.start(1000, self)
                print('Starting timer')
        if signal == 'Playlist.OnAdd':        
            gui.rpc("GUI.ShowNotification",{"title":"Added to playlist!", "message":param}, False)
        if signal == 'System.OnQuit' or signal == 'System.OnRestart':
            if self.timer.isActive():
                self.timer.stop()
                print('Stoping timer')
            self.quit(False)
        if signal == 'thumbnail':
            url = param.split('image://',1)[1]
            url = url[0:(len(url)-1)]
            url = urllib.parse.unquote(url)
            img_arr = urllib.request.urlopen(url).read()
            qImg = QImage()
            qImg.loadFromData(img_arr)
            self.img.setPixmap(QPixmap(qImg))
        if signal == 'time':
            param = json.loads(param)
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
            totTime = timeToDuration(totalTime)
            curTime = timeToDuration(time)
            if totTime>0:
                self.pbar.setValue((curTime/totTime)*100)
        #print (signal)


    def timerEvent(self, e):
            self.rpc("Player.GetProperties",{"playerid":1,"properties":["totaltime","time"]}, True)

            
    def showInputDialog(self):
        text, ok = QInputDialog.getText(self, 'Send Text', 
            'Type here what you want to send:')
        
        if ok:
            self.rpc("Input.SendText",{"text":str(text)}, False)
            
    
    def showHelpDialog(self):        
        h = HelpWidget()
        h.exec_()

    
    def keyPressEvent(self, e):        
        if e.key() == Qt.Key_Up:
            self.rpc("Input.Up",[], False)
        elif e.key() == Qt.Key_Down:
            self.rpc("Input.Down",[], False)
        elif e.key() == Qt.Key_Left:
            self.rpc("Input.Left",[], False)
        elif e.key() == Qt.Key_Right:
            self.rpc("Input.Right",[], False)
        elif e.key() == Qt.Key_F9:
            self.rpc("Input.ExecuteAction",{"action":"volumedown"}, False)
        elif e.key() == Qt.Key_F10:
            self.rpc("Input.ExecuteAction",{"action":"volumeup"}, False)
        elif e.key() == Qt.Key_F11:
            self.rpc("Input.ExecuteAction",{"action":"mute"}, False)
        elif e.key() == Qt.Key_Tab:
            self.rpc("Input.ExecuteAction",{"action":"fullscreen"}, False)
        elif e.key() == Qt.Key_Space:
            self.rpc("Input.ExecuteAction",{"action":"playpause"}, False)
        elif e.key() == Qt.Key_Control:
            if self.isPlaying:
                self.rpc("Input.ShowOSD",[], False)
        elif e.key() == Qt.Key_PageUp:
            self.rpc("Input.ExecuteAction",{"action":"pageup"}, False)
        elif e.key() == Qt.Key_PageDown:
            self.rpc("Input.ExecuteAction",{"action":"pagedown"}, False)
        elif e.key() == Qt.Key_Escape:
            self.rpc("Input.ExecuteAction",{"action":"parentfolder"}, False)
        elif e.key() == Qt.Key_Home:
            self.rpc("Input.Home",[], False)
        elif e.key() == Qt.Key_Backspace:
            self.rpc("Input.Back",[], False)
        elif e.key() == Qt.Key_Return:
            self.rpc("Input.Select",[], False)
        elif e.key() == Qt.Key_I:
            if self.isPlaying:
                self.rpc("Player.GetItem",{"playerid":1}, True)
            else:    
                self.rpc("Input.Info",[], False)
        elif e.key() == Qt.Key_Q:
            self.status.setText("Quiting now...")
            self.quit(True)
        elif e.key() == Qt.Key_A:
            self.rpc("Input.ExecuteAction",{"action":"queue"}, True)
        elif e.key() == Qt.Key_C:
            self.rpc("Input.ContextMenu",[], False)
        elif e.key() == Qt.Key_P:
            self.rpc("Input.ExecuteAction",{"action":"playlist"}, True)
        elif e.key() == Qt.Key_Z:
            self.rpc("Input.ExecuteAction",{"action":"aspectratio"}, False)
        elif e.key() == Qt.Key_Comma:
            self.rpc("Input.ExecuteAction",{"action":"stepback"}, False)
        elif e.key() == Qt.Key_Period:
            self.rpc("Input.ExecuteAction",{"action":"stepforward"}, False)
        elif e.key() == Qt.Key_BracketLeft:
            self.rpc("Input.ExecuteAction",{"action":"subtitledelayminus"}, False)
        elif e.key() == Qt.Key_BracketRight:
            self.rpc("Input.ExecuteAction",{"action":"subtitledelayplus"}, False)
        elif e.key() == Qt.Key_1:
            self.rpc("Addons.ExecuteAddon",{"addonid":"plugin.video.exodus"}, False)
        elif e.key() == Qt.Key_2:
            self.rpc("Addons.ExecuteAddon",{"addonid":"plugin.video.twitch"}, False)
        elif e.key() == Qt.Key_F1:
            self.showHelpDialog()
        elif e.key() == Qt.Key_Backslash:
            self.showInputDialog()
        
            #self.rpc("Addons.ExecuteAddon",{"addonid":"plugin.video.exodus","params":{"action":"seasons"}}, True)
            #self.rpc("GUI.ActivateWindow",{"window":"video", "parameters":["sources://video"]}, True)
    
    
    def rpc(self, method, params, should_respond):
        d = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            }
        if should_respond:
            d.update({"id":1})
        m = json.dumps(d)
        self.mySocket.send(m.encode())
    
    
    def quit(self, shutdownKodi):
        if self.responseThread.isRunning():
            #print("Killing thread")
            self.responseThread.terminate()
            
        print("Killed thread")
        
        if shutdownKodi:
            self.rpc("System.Shutdown",[], False)
            
        self.mySocket.close()
        print("Dropped tcp connection")    
        sys.exit(0) 



def timeToDuration(time):
    duration = time['hours']*3600 + time['minutes']*60 + time['seconds']
    return duration
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="The ip of the machine kodi is running on")
    parser.add_argument("-p", "--port", help="The port kodi is listening to", type=int)
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    gui = Gui()
    
    if args.ip:
        gui.params['ip'] = str(args.ip)
    else:
        gui.params['ip'] = "DEFAULT_IP_HERE"
    
    if args.port:
        gui.params['port'] = args.port
    else:
        gui.params['port'] = DEFAULT_PORT_HERE
    
    print("Initiating tcp connection")    
    gui.mySocket.connect((gui.params['ip'],gui.params['port']))
    
    gui.rpc("GUI.ShowNotification",{"title":"Daddy's home!", "message":"The only rightful owner"}, False)
    
    app.exec()
    gui.quit(False)
