import sys, socket, json, urllib.request, argparse
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QDialog, QLabel, QProgressBar, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, QBasicTimer
from ResponseThread import ResponseThread
from HelpDialog import HelpDialog
from OpenDialog import OpenDialog
from utilities import *

class Gui(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.mySocket = socket.socket()
        self.params = {}
        self.responseThread = ResponseThread(self.mySocket)
        self.isPlaying = False
        
        self.setGeometry(300, 200, 300, 200)
        self.setWindowTitle('Kodi Remote Control')
        self.setWindowIcon(QIcon(ICON_PATH))
        
        self.img = QLabel('img')
        self.img.setPixmap(QPixmap(IMG_PATH))
        
        self.status = QLabel('OK')
        
        self.pbar = QProgressBar()
        self.progress = 0
        
        self.timer = QBasicTimer()
        
        box = QVBoxLayout()
        box.setSpacing(10)
        
        box.addWidget(self.img, Qt.AlignCenter)
        box.addWidget(self.status, Qt.AlignLeft)
        box.addWidget(self.pbar)
        
        self.setLayout(box)
        self.show()
        self.setFixedSize(self.size())
        
        self.responseThread.mySignal.connect(self.handleSignals)
        self.responseThread.start()
        

    def handleSignals(self, signal, param):
        if signal == 'Input.OnInputRequested':
            self.showInputDialog()
            print("Text sending")
        if signal == 'Player.OnStop':
            self.isPlaying = False
            self.status.setText( 'Nothing playing now' )
            self.img.setPixmap(QPixmap(IMG_PATH))
            if self.timer.isActive():
                self.timer.stop()
                self.pbar.setValue(0)
                print('Stoping timer')
        if signal == 'play':
            self.isPlaying = True
            self.status.setText( param )
            self.rpc("Player.GetItem",{"properties":["thumbnail","fanart"],"playerid":1}, True)
            if not self.timer.isActive():
                self.timer.start(1000, self)
                print('Starting timer')
        if signal == 'queue':        
            gui.rpc("GUI.ShowNotification",{"title":"Added to playlist!", "message":param}, False)
        if signal == 'System.OnQuit' or signal == 'System.OnRestart':
            if self.timer.isActive():
                self.timer.stop()
                print('Stoping timer')
            self.quit(False)
        if signal == 'thumbnail':
            url = urllib.parse.unquote(param)
            try:
                img_arr = urllib.request.urlopen(url).read()
                qImg = QImage()
                qImg.loadFromData(img_arr)
                self.img.setPixmap(QPixmap(qImg))
            except Exception as e:
                print("---> Error while getting image: %s" % e)
        if signal == 'time':
            tokens = param.split('-',1)
            curTime = int(tokens[0])
            totTime = int(tokens[1])
            if totTime>0:
                self.pbar.setValue((curTime/totTime)*100)
        if signal == 'addons':
            OpenDialog(param, self).exec_()
        #print (signal)


    def timerEvent(self, e):
            self.rpc("Player.GetProperties",{"playerid":1,"properties":["totaltime","time"]}, True)

            
    def showInputDialog(self):
        text, ok = QInputDialog.getText(self, 'Send Text', 
            'Type here what you want to send:')
        
        if ok:
            self.rpc("Input.SendText",{"text":str(text)}, False)
            
    
    def showHelpDialog(self):        
        HelpDialog().exec_()

    
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
        elif e.key() == Qt.Key_O:
            self.rpc("Addons.GetAddons",{"content":"video"}, True)
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
        elif e.key() == Qt.Key_Equal:
            self.rpc("Input.ExecuteAction",{"action":"volampup"}, False)
        elif e.key() == Qt.Key_Minus:
            self.rpc("Input.ExecuteAction",{"action":"volampdown"}, False)
        elif e.key() == Qt.Key_1:
            self.rpc("Addons.ExecuteAddon",{"addonid":"plugin.video.exodus"}, False)
        elif e.key() == Qt.Key_2:
            self.rpc("Addons.ExecuteAddon",{"addonid":"plugin.video.twitch"}, False)
        elif e.key() == Qt.Key_F1:
            self.showHelpDialog()
        elif e.key() == Qt.Key_Backslash:
            self.showInputDialog()
            
    
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
        gui.params['ip'] = DEFAULT_IP
    
    if args.port:
        gui.params['port'] = args.port
    else:
        gui.params['port'] = DEFAULT_PORT
    
    print("Initiating tcp connection")    
    gui.mySocket.connect((gui.params['ip'],gui.params['port']))
    
    gui.rpc("GUI.ShowNotification",{"title":"Remote Control Connection", "message":TOAST}, False)
    
    app.exec()
    gui.quit(False)
