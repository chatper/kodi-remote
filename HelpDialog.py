from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPalette
from PyQt5.QtCore import Qt
from utilities import *

class HelpDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        
        self.setGeometry(600, 200, 420, 320)
        self.setWindowTitle('Help')
        self.setWindowIcon(QIcon(ICON_PATH))
        
        label = QLabel('Press anything on your keyboard to see what it does.')
        self.actionLabel = QLabel('Press something!')
        self.img = QLabel('img', self)
        self.img.setPixmap(QPixmap(HELP_IMG_PATH))
        
        
        grid = QGridLayout()
        grid.setSpacing(4)
        
        grid.addWidget(self.img, 0, 0)
        grid.addWidget(label, 1, 0)
        grid.addWidget(self.actionLabel, 2, 0)
        
        myFont=QFont()
        myFont.setBold(True)
        myFont.setPixelSize(24)
        self.actionLabel.setFont(myFont)
        
        palette = QPalette()
        palette.setColor(QPalette.Foreground,Qt.green)
        self.actionLabel.setPalette(palette)
        
        self.setLayout(grid)
        self.show()

    def keyPressEvent(self, e): 
        if e.key() == Qt.Key_Up:
            self.actionLabel.setText('Used for navigation - Up')
        elif e.key() == Qt.Key_Down:
            self.actionLabel.setText('Used for navigation - Down')
        elif e.key() == Qt.Key_Left:
            self.actionLabel.setText('Used for navigation - Left')
        elif e.key() == Qt.Key_Right:
            self.actionLabel.setText('Used for navigation - Right')
        elif e.key() == Qt.Key_F1:
            self.actionLabel.setText('Help')
        elif e.key() == Qt.Key_F9:
            self.actionLabel.setText('Volume Down')
        elif e.key() == Qt.Key_F10:
            self.actionLabel.setText('Volume Up')
        elif e.key() == Qt.Key_F11:
            self.actionLabel.setText('Toggle Mute')
        elif e.key() == Qt.Key_Tab:
            self.actionLabel.setText('Toggle Fullscreen')
        elif e.key() == Qt.Key_Space:
            self.actionLabel.setText('Play/Pause')
        elif e.key() == Qt.Key_Control:
            self.actionLabel.setText('Toggle Player HUD - Only works if something is playing')
        elif e.key() == Qt.Key_PageUp:
            self.actionLabel.setText('Page Up')
        elif e.key() == Qt.Key_PageDown:
            self.actionLabel.setText('Page Down')
        elif e.key() == Qt.Key_Escape:
            self.actionLabel.setText('Navigate to parent directory')
        elif e.key() == Qt.Key_Home:
            self.actionLabel.setText('Home menu')
        elif e.key() == Qt.Key_Backspace:
            self.actionLabel.setText('Back')
        elif e.key() == Qt.Key_Return:
            self.actionLabel.setText('Select')
        elif e.key() == Qt.Key_I:
            self.actionLabel.setText('Information dialog')
        elif e.key() == Qt.Key_Q:
            self.actionLabel.setText('Quit application AND shutdown Kodi')
        elif e.key() == Qt.Key_A:
            self.actionLabel.setText('Add to playlist')
        elif e.key() == Qt.Key_C:
            self.actionLabel.setText('Context dialog')
        elif e.key() == Qt.Key_P:
            self.actionLabel.setText('Show playlist if exists')
        elif e.key() == Qt.Key_O:
            self.actionLabel.setText('Show a list of video addons available and open the selection')
        elif e.key() == Qt.Key_Z:
            self.actionLabel.setText('Change aspect ration')
        elif e.key() == Qt.Key_Comma:
            self.actionLabel.setText('Step back - Only works if something is playing')
        elif e.key() == Qt.Key_Period:
            self.actionLabel.setText('Step forward - Only works if something is playing')
        elif e.key() == Qt.Key_BracketLeft:
            self.actionLabel.setText('Subtitle delay minus')
        elif e.key() == Qt.Key_BracketRight:
            self.actionLabel.setText('Subtitle delay plus')
        elif e.key() == Qt.Key_Equal:
            self.actionLabel.setText('Amplify volume up')
        elif e.key() == Qt.Key_Minus:
            self.actionLabel.setText('Amplify volume down')
        elif e.key() == Qt.Key_Backslash:
            self.actionLabel.setText('Send string to Kodi')
        else:
            if e.key() >= 48 and e.key() <=57:
                self.actionLabel.setText('Activate addons - Usually used after shortcut O')
            else:
                self.actionLabel.setText('No action is assigned to that key')
