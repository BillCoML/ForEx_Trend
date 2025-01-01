
from controller import *

from PyQt6.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtWidgets import QTableView

from modules.transformed_data_model import *
from modules.predict_options import *

class View_Transformed_Data(QMainWindow):
    '''
    This window shows all transformed data
    '''
    def __init__(self, parent: 'View_Modify', controller: 'Controller'):
        super().__init__()
        self.parent = parent
        self.controller = controller

        #Set title and dimension
        self.setWindowTitle("View Transformed Data")
        self.resize(490, 500)
        self.move(0, 0)

        self.transformed_data_table = QTableView()
        self.transformed_data_model = TransformedDataModel(self.controller)
        self.transformed_data_table.setModel(self.transformed_data_model)

        self.go_back_button = QPushButton("Back")
        self.predict_button = QPushButton("Predict Options")

        self.go_back_button.clicked.connect(self.go_back_button_clicked)
        self.predict_button.clicked.connect(self.predict_button_clicked)


        layout = QVBoxLayout()
        sub_layout = QGridLayout()
        sub_layout.addWidget(self.go_back_button, 0, 0)
        sub_layout.addWidget(self.predict_button, 0, 1)

        layout.addWidget(self.transformed_data_table)
        layout.addLayout(sub_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.transformed_data_model.list_data()
        self.transformed_data_table.setColumnWidth(0, 120) #Date
        self.transformed_data_table.setColumnWidth(1, 100) #High
        self.transformed_data_table.setColumnWidth(2, 100) #Low
        self.transformed_data_table.setColumnWidth(3, 100) #Close

    def go_back_button_clicked(self):
        '''
        Redirect to View and Modify
        '''
        self.hide()
        self.parent.show()

    def predict_button_clicked(self):
        '''
        Directs to a menu of options for predictions.
        '''
        #self.hide()
        self.window = Predict_Options(self, self.controller)
        self.window.show()



