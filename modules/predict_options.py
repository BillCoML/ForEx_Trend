
from controller import *

from PyQt6.QtWidgets import QMainWindow, QGridLayout
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QCheckBox

from modules.view_predictions import *

class Predict_Options(QMainWindow):
    '''
    There will be some choices to make in order to predict such as:
    + Start and end indices in the data
    + How many time points to predict?
    '''
    def __init__(self, parent: 'View_Transformed_Data', controller: 'Controller'):
        super().__init__()
        self.parent = parent
        self.controller = controller

        self.setWindowTitle("Predict Options")
        #Specify location
        self.resize(200, 300)
        self.move(500, 0)

        #Note that start index must always be smaller than end index (because the latest data is on top)
        start_label = QLabel("Start Index")
        self.start_text = QLineEdit() #Only allows integer
        end_label = QLabel("End Index")
        self.end_text = QLineEdit() #Only allows integer

        n_points_label = QLabel("Time Steps")
        self.n_points_text = QLineEdit() #Only allows integer

        self.go_back_button = QPushButton("Back")
        self.predict_button = QPushButton("Predict")

        layout = QGridLayout()

        layout.addWidget(start_label, 0, 0)
        layout.addWidget(self.start_text, 0, 1)
        layout.addWidget(end_label, 1, 0)
        layout.addWidget(self.end_text, 1, 1)
        
        layout.addWidget(n_points_label, 2, 0)
        layout.addWidget(self.n_points_text, 2, 1)
        
        layout.addWidget(self.go_back_button, 3, 0)
        layout.addWidget(self.predict_button, 3, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #Link buttons to functionalities
        self.go_back_button.clicked.connect(self.go_back_button_clicked)
        self.predict_button.clicked.connect(self.predict_button_clicked)
        


    def go_back_button_clicked(self):
        '''
        Redirect to the view transform page
        '''
        self.hide()
        self.parent.show()

    def predict_button_clicked(self):
        '''
        Reads the input and if prediction can be made, will show a table of values only of those N values
        '''
        try:
        
            start = self.start_text.text()
            end = self.end_text.text()
            n_points = self.n_points_text.text()

            #Inputs need to be validated
            selected_data = self.controller.validate_prediction_options(start=start, end=end, n_points=n_points)

            #After a part of transformed data frame is selected, it has to be recoded into integers as prediction inputs
            re_low, re_high, re_close = self.controller.recode_data(selected_data)

            predicted_data = self.controller.iterative_prediction(re_low=re_low, re_high=re_high, re_close=re_close, use_string_code = True)

            self.hide()
            self.window = View_Predictions(self, predicted_data=predicted_data, controller=self.controller)
            self.window.show()
            

        except ExceedContextLengthError:
            QMessageBox.warning(self, "Fail", f"Time range exceeds the maximum of {self.controller.max_points}")

        except ValidatePredictionOptionsError:
            QMessageBox.warning(self, "Fail", "Invalid Inputs")

        except PredictError:
            QMessageBox.warning(self, "Fail", "Prediction failed")