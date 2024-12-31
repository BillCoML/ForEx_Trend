
from controller import *

from PyQt6.QtCore import Qt, QAbstractTableModel


class RawDataModel(QAbstractTableModel):

    def __init__(self, controller:'Controller'):
        super().__init__()
        self.controller = controller
        self.raw_data = self.controller.read_raw_data()
        self._data = []

    
    def list_data(self):
        '''
        Fetches data from the raw file 
        '''
        self._data = []
        for _ in range(len(self.raw_data)):
            row = self.raw_data.iloc[_]
            one_point = [row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Change(Pips)'], row['Change(%)']]
            self._data.append(one_point)
        
        self.layoutChanged.emit()

    def data(self, index, role):
        value = self._data[index.row()][index.column()]
        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value, float):
                if index.column() == 5:
                    return "%d" % value
                if index.column() == 6:
                    return "%.2f" % value
                else:
                    return "%.2f" % value
            
            if isinstance(value, str):
                return "%s" % value
            
            return value
        
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(value, int) or isinstance(value, float):
                return Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight
    
    def flags(self, index):
        '''
        Make cells editable when "Modify" is set
        "Modify" becomes "Save"
        '''
        if index.column() in [1, 2, 3, 4]:
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
    
    def setData(self, index, value, role):
        '''
        Updates data when a cell is edited
        '''
        if role == Qt.ItemDataRole.EditRole:
            column = index.column()
            try:
                # Convert and set values based on column type
                if column in [1, 2, 3, 4, 5, 6]:  # Numeric columns
                    self._data[index.row()][column] = float(value)

                else:
                    self._data[index.row()][index.column()] = str(value)
                
                self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])
                return True
            except ValueError:
                return False  # Handle invalid input gracefully
        return False
    
    def save_to_file(self):

        '''
        When Save button is triggered, save to file and refresh data
        '''
        
        self.raw_data['Date'] = [row[0] for row in self._data]
        self.raw_data['Open'] = [row[1] for row in self._data]
        self.raw_data['High'] = [row[2] for row in self._data]
        self.raw_data['Low']  = [row[3] for row in self._data]
        self.raw_data['Close'] = [row[4] for row in self._data]

        #The change in pip will be automatically calculated
        self.raw_data['Change(Pips)'] = [(row[4]-row[1])*100 for row in self._data]
        self.raw_data['Change(%)'] = [round( 100*((row[4]/row[1]) - 1), 2) for row in self._data]

        self.raw_data.to_csv(self.controller.raw_file_name, index=False)

        #After saving completes, refresh data so Change in Pips and % is refreshed

        self.list_data()

            
    def rowCount(self, index):
        '''
        Returns number of rows in the table
        '''
        return len(self._data)
    
    def columnCount(self, index):
        '''
        Returns number of columns in the table
        '''
        if self._data:
            return len(self._data[0])
        
        else:
            return 0
        
    def headerData(self, section, orientation, role = Qt.ItemDataRole.DisplayRole):
        """
        Returns the headers for the table
        i.e: Column names
        """
        headers = ['Date', 'Open', 'High', 'Low', 'Close', 'Change(Pips)', 'Change(%)']
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return "%s" % headers[section]
        return super().headerData(section, orientation, role) 
        

        