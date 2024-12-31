
from exception.data_transformation_exception import DataTransformationError
from exception.read_data_exception import ReadDataError
from exception.file_format_exception import FileFormatError
from exception.data_addition_exception import AddDataError
from exception.prediction_options_exception import ValidatePredictionOptionsError
from exception.context_length_exception import ExceedContextLengthError
from exception.predict_exception import PredictError

from FXmodel.close_model import *
from FXmodel.low_model import *
from FXmodel.high_model import *
from FXmodel.layers.recode import *

import os
import pandas as pd
from datetime import datetime, timedelta


class Controller:
    def __init__(self):
        
        self.raw_file_name = None
        self.transformed_file_name = 'data/transformed_data.csv'

        #For predictions
        self.n_points = None
        self.max_points = 96 #The maximum context window
        self.start = None
        self.end = None
          

        #Delete this file before a new file is imported
        if os.path.exists(self.transformed_file_name):
            os.remove(self.transformed_file_name)


    def read_raw_data(self):
        '''
        Read the data from raw file (original file)
        '''
        try:
            data = pd.read_csv(self.raw_file_name, index_col=False)
            return data
        except Exception:
            raise ReadDataError("Cannot read raw file")
        
    def read_transformed_data(self):
        '''
        Read the data from the transform file,
        No failure can happen if you already get to this step
        '''
        try:
            data = pd.read_csv(self.transformed_file_name, index_col=False)
            return data
        except Exception:
            raise ReadDataError("Cannot read transform file")


    def find_file(self, file_name):
        '''
        For now, all files imported must be from FxBooks.com because 
        the format matters
        '''
        if os.path.exists(file_name):
            if file_name[-4:] == '.csv':
                self.raw_file_name = file_name
            
            else:
                raise FileFormatError()
            
        else:
            raise FileNotFoundError()
    
    def add_data(self, new_data:dict):
        '''
        Add data to csv file, data received from GUI
        The format is ['Date', 'Open', 'High', 'Low', 'Close']
        '''
        try:
            #Casting data first
            new_data["Open"] = float(new_data["Open"])
            new_data["High"] = float(new_data["High"])
            new_data["Low"] = float(new_data["Low"])
            new_data["Close"] = float(new_data["Close"])

            #If data are not of the right type, there will be exceptions
            new_data["Change(Pips)"] = round((new_data['Close']-new_data['Open']) * 100, 1)
            new_data["Change(%)"] = round( 100*((new_data['Close'] / new_data['Open']) - 1), 2)

            #Now ADD data and SAVE to csv file
            data = self.read_raw_data()
            new_data_df = pd.DataFrame([new_data])
            updated_data = pd.concat([new_data_df, data], ignore_index=True)
            updated_data.to_csv(self.raw_file_name, index=False)

        except:
            raise AddDataError()
        

    def transform_data(self):
            
        try:
            data = self.read_raw_data()

            #Copy over to a new df, raw file untouched

            df = data.copy(deep=False)

            #Formula for pips change

            df['High'] = (df['High'] - df['Open']) * 100
            df['Low'] = (df['Low'] - df['Open']) * 100
            df['Close'] = (df['Close'] - df['Open']) * 100

            df['High'] = df['High'].round(1)
            df['Low'] = df['Low'].round(1)
            df['Close'] = df['Close'].round(1)

            #Select relevant columns for predictions

            df = df[['Date','High','Low','Close']]

            #Export to a new file for predictions

            df.to_csv(self.transformed_file_name, index=False)

        except Exception:
            raise DataTransformationError()
        

    def get_next_time(self, top_time:str, extra_mins=30):
        '''
        Get date and time of the next ... mins
        The function receives the very top datetime data.
        '''
        date_time_list = top_time.split()
        date = date_time_list[0].split('/')
        time = date_time_list[1].split(':')
        
        #Extract date
        mm = int(date[0])
        dd = int(date[1])
        yyyy = int(date[2])
    
        #Extract time
        hour = int(time[0])
        min = int(time[1])

        current_top_time = datetime(year=yyyy, month=mm, day=dd, hour=hour, minute=min)

        #Reformat the time
        next_time = ( current_top_time + timedelta(minutes=extra_mins) ).strftime('%m/%d/%Y %H:%M')

        return next_time
    
    def get_top_time(self):
        '''
        Returns the latest date time
        '''
        data = self.read_transformed_data()
        top_time = data['Date'][0]
        
        return top_time
    
    def get_time_index(self, index):
        '''
        Returns the time at index (from 1)
        '''
        data = self.read_transformed_data()
        top_time = data['Date'][index-1]
        
        return top_time

    
    def validate_prediction_options(self, **kwargs):
        
        try:
            data = self.read_transformed_data() 

            start = int( kwargs['start'] )
            end = int( kwargs['end'] )
            n_points = int( kwargs['n_points'] )

            #If the range is not possible, will raise ValidatePredictionOptionsError
            selected_data = data.iloc[start-1: end]

            m = end - start + 1

            #Check if start < end
            if start >= end:
                raise AssertionError()

            #Check if the input exceeds context length
            if m + n_points > self.max_points:
                raise ExceedContextLengthError()
            
            self.n_points = n_points
            self.start = start

            return selected_data
        
        except ExceedContextLengthError:

            raise ExceedContextLengthError()
        
        except:
            '''
            General exceptions
            '''
            raise ValidatePredictionOptionsError()
    
    def recode_close(self, array, x1, x2):

        conditions = [
            array < -x2,
            (array >= -x2) & (array < -x1),

            (array >= -x1) & (array <= x1),
            
            (array > x1) & (array <= x2),
            array > x2
        ]

        # Define the corresponding values for each condition
        values = [0, 1, 2, 3, 4]

        # Apply np.select to assign values based on conditions
        result = np.select(conditions, values)

        return result.astype('int8')
    

    def recode_low_high(self, array, x1, x2):

        arr = np.abs(array)

        conditions = [
            arr <= x1, 
            (arr > x1) & (arr <= x2),
            arr > x2
        ]

        # Define the corresponding values for each condition
        values = [0, 1, 2]

        # Apply np.select to assign values based on conditions
        result = np.select(conditions, values)

        return result.astype('int8')
    

    def recode_data(self, data):
        #First need to extract data
        high = data['High'].to_numpy()[::-1]
        close = data['Close'].to_numpy()[::-1]
        low = data['Low'].to_numpy()[::-1]

        #Need to recode first

        print(high)

        re_low = self.recode_low_high(low, 43, 216)
        re_high = self.recode_low_high(high, 43, 216)
        re_close = self.recode_close(close, 43, 216)

        return re_low, re_high, re_close
    

    def build_models(self):
        '''
        Initialized model only once at start
        '''
        self.low_model = Low_Model()
        self.high_model = High_Model()
        self.close_model = Close_Model()


    def predict(self, **kwargs):
        '''
        Predict function receives tensor recoded as .npy (concatenated) so we need a function for it in kwargs
        '''

        try:
        
            next_low = self.low_model.predict(**kwargs)
            next_high = self.high_model.predict(**kwargs)
            next_close = self.close_model.predict(**kwargs)

            return next_low, next_high, next_close
        
        except:
            raise PredictError()
        

    def iterative_prediction(self, **kwargs):
        '''
        Ordinary and the fastest prediction method
        '''

        re_low = kwargs['re_low']
        re_high = kwargs['re_high']
        re_close = kwargs['re_close']

        use_string_code = kwargs['use_string_code']

        predicted_data = pd.DataFrame([])

        top_time = self.get_time_index(index=self.start)

        for _ in range(1, self.n_points+1):
            '''
            Before every refresh, we need to generate data
            '''

            next_time = self.get_next_time(top_time = top_time)

            top_time = next_time

            #It may take some time for each prediction

            next_low, next_high, next_close = self.predict(re_low=re_low, re_high=re_high, re_close=re_close)

            #after one generation is done, new_data need to be added to the previous data so we can get the next new prediction
            re_low = np.append(re_low, next_low)
            re_high = np.append(re_high, next_high)
            re_close = np.append(re_close, next_close)


            new_data =  {
                            'Date': next_time, 

                            'High': next_high, 
                            'Low': next_low, 
                            'Close': next_close
                        }
            
            
            new_data_df = pd.DataFrame([new_data])

            predicted_data = pd.concat([new_data_df, predicted_data], ignore_index=True)


        if (use_string_code):

            self.string_code(predicted_data)


        return predicted_data


    def string_code(self, dataframe):
        '''
        Instead of predictions as integer, better appearances can be signs
        '''
        dataframe["Low"] = dataframe["Low"].replace({0:'', 1: '-', 2: '- -'})
        dataframe["High"] = dataframe["High"].replace({0:'', 1: '+', 2: '+ +'})
        dataframe["Close"] = dataframe["Close"].replace({0:'- -', 1: '-', 2: '', 3: '+', 4: '+ +'})


        


        






