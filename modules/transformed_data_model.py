
from PyQt6.QtCore import Qt, QAbstractTableModel


class TransformedDataModel(QAbstractTableModel):

    def __init__(self, controller:"Controller"):
        super().__init__()
        self.controller = controller
        self.transformed_data = self.controller.read_transformed_data()
        self._data = []

    
    def list_data(self):
        '''
        Fetches data from the raw file 
        '''
        self._data = []
        for _ in range(len(self.transformed_data)):
            row = self.transformed_data.iloc[_]
            one_point = [row['Date'], row['High'], row['Low'], row['Close']]
            self._data.append(one_point)
        
        self.layoutChanged.emit()

    def data(self, index, role):
        value = self._data[index.row()][index.column()]
        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value, float):
                return "%d" % value
    
            if isinstance(value, str):
                return "%s" % value
            
            return value
        
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(value, int) or isinstance(value, float):
                return Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight

            
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
        headers = ['Date', 'High', 'Low', 'Close']
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return "%s" % headers[section]
        return super().headerData(section, orientation, role) 
        

        