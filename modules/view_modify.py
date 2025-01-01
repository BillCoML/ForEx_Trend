
from controller import *

from PyQt6.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QWidget, QPushButton, QMessageBox
from PyQt6.QtWidgets import QTableView

from modules.view_transformation import *
from modules.raw_data_model import *
from modules.add_next_data import *

class View_Modify(QMainWindow):
    '''
    This window shows all raw data, user can view and modify if needed. 
    Table model is used for this window.
    '''
    def __init__(self, parent: 'File_Import', controller: 'Controller'):
        super().__init__()
        self.parent = parent
        self.controller = controller
        self.setWindowTitle("View and Modify")
        
        #Specify location
        self.resize(860, 500)
        self.move(0, 0)

        self.raw_data_table = QTableView()
        self.raw_data_model = RawDataModel(self.controller)
        self.raw_data_table.setModel(self.raw_data_model)

        self.go_back_button = QPushButton("Back")
        self.modify_data_button = QPushButton("Modify")
        self.add_data_button = QPushButton("Add Next")
        self.transform_data_button = QPushButton("Transform")

        self.go_back_button.clicked.connect(self.go_back_button_clicked)
        self.modify_data_button.clicked.connect(self.modify_data_button_clicked)
        self.add_data_button.clicked.connect(self.add_data_button_clicked)
        self.transform_data_button.clicked.connect(self.transform_data_button_clicked)

        layout = QVBoxLayout()
        sub_layout = QGridLayout()
        sub_layout.addWidget(self.modify_data_button, 0, 0)
        sub_layout.addWidget(self.add_data_button, 0, 1)
        sub_layout.addWidget(self.go_back_button, 1, 0)
        sub_layout.addWidget(self.transform_data_button, 1, 1)

        layout.addWidget(self.raw_data_table)
        layout.addLayout(sub_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.raw_data_model.list_data()
        self.raw_data_table.setColumnWidth(0, 200)
        self.raw_data_table.setColumnWidth(1, 100)
        self.raw_data_table.setColumnWidth(2, 100)
        self.raw_data_table.setColumnWidth(3, 100)
        self.raw_data_table.setColumnWidth(4, 100)
        self.raw_data_table.setColumnWidth(5, 100)
        self.raw_data_table.setColumnWidth(6, 100)

    def go_back_button_clicked(self):
        '''
        Redirect to File Import
        '''
        self.hide()
        self.parent.show()

    def modify_data_button_clicked(self):
        '''
        If Modify is triggered, all changes to the data will be exported to the raw file.
        '''
        self.raw_data_model.save_to_file()
        QMessageBox.information(self, "Success", "Data modified")

    def add_data_button_clicked(self):
        '''
        If add is triggered, it directs to another page just to add the next data, no hiding is used
        '''
        self.hide()
        self.window = Add_Data(self, self.controller)
        self.window.show()

    def transform_data_button_clicked(self):
        '''
        Direct to transformed data table
        '''
        try:
            self.controller.transform_data()
            self.hide()
            self.window = View_Transformed_Data(self, self.controller)
            self.window.show()

        except DataTransformationError:
            QMessageBox.warning(self, "Error", "Cannot Transform data")