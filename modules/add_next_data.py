from controller import *

from PyQt6.QtWidgets import QMainWindow, QGridLayout
from PyQt6.QtWidgets import QWidget, QPushButton, QMessageBox, QLabel, QLineEdit

class Add_Data(QMainWindow):
    '''
    This window only has editable cells, with DATE and TIME already specified,
    user only has to input Open, Low, High and Close
    '''

    def __init__(self, parent: 'View_Modify', controller: 'Controller'):
        super().__init__()
        self.parent = parent
        self.controller = controller

        self.setWindowTitle("Adding New Data")
        #Specify location
        self.resize(200, 300)
        self.move(0, 0)

        #We need to fill in Date cell with a value
        data = self.controller.read_raw_data()
        top_time = data["Date"][0]
        self.next_time = self.controller.get_next_time(top_time=top_time, extra_mins=15)

        #Fields to input values
        date_label = QLabel("Date-Time:")
        self.date_time_text = QLabel(self.next_time)
        open_label = QLabel("Open")
        self.open_text = QLineEdit()
        high_label = QLabel("High")
        self.high_text = QLineEdit()
        low_label = QLabel("Low")
        self.low_text = QLineEdit()
        close_label = QLabel("Close")
        self.close_text = QLineEdit()

        #buttons
        self.go_back_button = QPushButton("Back")
        self.add_button = QPushButton("Add")

        layout = QGridLayout()

        layout.addWidget(date_label, 0, 0)
        layout.addWidget(self.date_time_text, 0, 1)

        layout.addWidget(open_label, 1, 0)
        layout.addWidget(self.open_text, 1, 1)

        layout.addWidget(high_label, 2, 0)
        layout.addWidget(self.high_text, 2, 1)

        layout.addWidget(low_label, 3, 0)
        layout.addWidget(self.low_text, 3, 1)

        layout.addWidget(close_label, 4, 0)
        layout.addWidget(self.close_text, 4, 1)


        layout.addWidget(self.go_back_button, 5, 0)
        layout.addWidget(self.add_button, 5, 1)

        #Connect button to functionalities
        self.go_back_button.clicked.connect(self.go_back_button_clicked)
        self.add_button.clicked.connect(self.add_button_clicked)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def go_back_button_clicked(self):
        '''
        Redirect to View_Modify window
        '''
        self.hide()
        #Before the parent window pops up, all the data needs to be refreshed
        self.parent.__init__(self.parent.parent, self.controller)
        self.parent.show()

    def add_button_clicked(self):
        '''
        Calls add of controller
        '''
        try:
            #Extract values and save to file
            new_data = {"Date":self.next_time,
                        "Open":self.open_text.text(),
                        "High":self.high_text.text(),
                        "Low":self.high_text.text(),
                        "Close":self.close_text.text()}

            #If operations are invalid, exception will be raised by this
            self.controller.add_data(new_data)

            QMessageBox.information(self, "Success", "New Data Added")
        
        except AddDataError:

            QMessageBox.warning(self, "Failed", "Invalid Input")

        finally:
            #After add_button is clicked, always go back to see the modified data
            #...Now everytime going back we want it to reload the data!
            self.go_back_button_clicked()


