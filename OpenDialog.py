from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from utilities import *

class OpenDialog(QDialog):
    
    def __init__(self, addons, parent):
        super().__init__()
        
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Open Addon')
        self.setWindowIcon(QIcon(ICON_PATH))
        
        label = QLabel('Choose the addon you want to open.')
        
        grid = QGridLayout()
        grid.setSpacing(4)
        
        grid.addWidget(label, 0, 0)
        
        self.addonList = addons.split('-')
        self.addonList.remove('')
        self.parent = parent
        
        for i,j in enumerate(self.addonList):
            l = QLabel(str(i)+' -> '+j)
            grid.addWidget(l, i+1, 0)
            
        self.setLayout(grid)
        self.show()
        

    def keyPressEvent(self, e):
        if e.key() >= 48 and e.key() <=57:
            if len(self.addonList) > e.key() - 48:
                self.parent.rpc("Addons.ExecuteAddon",{"addonid":self.addonList[e.key() - 48]}, False)
        self.close()
