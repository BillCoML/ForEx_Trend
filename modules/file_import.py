from controller import *
from PyQt6.QtWidgets import QMainWindow, QGridLayout
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox

from modules.view_modify import *

class File_Import(QMainWindow):

    def __init__(self, parent: 'FXTrend', controller: 'Controller'):

        super().__init__()
        self.parent = parent
        self.controller = controller
        self.setWindowTitle("File Import")
        self.move(0, 0)
        self.resize(300, 200)

        file_label = QLabel("File Path")
        self.file_path_text = QLineEdit()
        self.go_back_button = QPushButton("Back")
        self.import_file_button = QPushButton("Import")

        layout = QGridLayout()
        layout.addWidget(file_label, 0, 0)
        layout.addWidget(self.file_path_text, 0, 1)
        layout.addWidget(self.go_back_button, 1, 0)
        layout.addWidget(self.import_file_button, 1, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.go_back_button.clicked.connect(self.go_back_button_clicked)
        self.import_file_button.clicked.connect(self.import_file_button_clicked)
    
    def go_back_button_clicked(self):
        '''
        Redirect to main menu
        '''
        self.hide()
        self.parent.show()

    def import_file_button_clicked(self):
        '''
        Find file, if accepted, direct to VIEW WINDOW
        '''
        try:
            file_name = self.file_path_text.text()
            self.controller.find_file(file_name)
            self.controller.read_raw_data()#Doesnt need to return anything, just to make sure read is safe

            #File found, now direct to View Table
            self.hide()
            self.window = View_Modify(self, self.controller)
            self.window.show()


        except FileFormatError:
            QMessageBox.warning(self, "Error", "Must be a .csv file")

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "File Not Found")

        except ReadDataError:
            QMessageBox.warning(self, "Error", "Cannot read data")
