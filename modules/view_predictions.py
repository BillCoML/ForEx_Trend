
from controller import *

from PyQt6.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtWidgets import QTableView

from modules.predicted_data_model import *
from modules.predict_options import *

class View_Predictions(QMainWindow):
    '''
    This window shows all predicted data
    '''
    def __init__(self, parent: 'Predict_Options', predicted_data, controller: 'Controller'):
        super().__init__()
        self.parent = parent
        self.controller = controller

        #Set title and dimension
        self.setWindowTitle("View Predictions")
        self.resize(450, 300)
        self.move(500, 0)

        self.predicted_data_table = QTableView()
        self.predicted_data_model = PredictedDataModel(predicted_data=predicted_data, controller=self.controller)
        self.predicted_data_table.setModel(self.predicted_data_model)

        self.go_back_button = QPushButton("Back")

        self.go_back_button.clicked.connect(self.go_back_button_clicked)


        layout = QVBoxLayout()
        sub_layout = QGridLayout()
        sub_layout.addWidget(self.go_back_button)

        layout.addWidget(self.predicted_data_table)
        layout.addLayout(sub_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.predicted_data_model.list_data()
        self.predicted_data_table.setColumnWidth(0, 130) #Date
        self.predicted_data_table.setColumnWidth(1, 100) #High
        self.predicted_data_table.setColumnWidth(2, 100) #Low
        self.predicted_data_table.setColumnWidth(3, 100) #Close

    def go_back_button_clicked(self):
        '''
        Redirect to Options=
        '''
        self.hide()
        self.parent.show()



