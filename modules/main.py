
from controller import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton

from modules.file_import import *

class FXTrend(QMainWindow):
    '''
    The first window when app is run, only two options of start or quit
    '''
    def __init__(self):

        super().__init__()
        self.controller = Controller()

        
        ###### Build model here #####
        self.controller.build_models()
        ##############################


        self.move(0, 0) #This helps to locate the window at a specific place across the game
        self.resize(300, 200)
        layout = QVBoxLayout()
        
        welcome = QLabel("Welcome to FXTrend")
        self.start_button = QPushButton("Start")
        self.quit_button = QPushButton("Quit")

        layout.addWidget(welcome)
        layout.addWidget(self.start_button)
        layout.addWidget(self.quit_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.start_button.clicked.connect(self.start_button_clicked)
        self.quit_button.clicked.connect(self.quit_button_clicked)

    def start_button_clicked(self):
        '''
        Direct to file import window
        '''
        self.hide()
        self.window = File_Import(self, self.controller)
        self.window.show()
    
    def quit_button_clicked(self):
        '''
        Simply quit the program, we can remove file before leaving
        '''
        QApplication.quit()


