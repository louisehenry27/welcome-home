from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd
from dateutil.parser import parse

class Sheet:
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    def __init__(self,sheet_key):
        self.sheet_key = sheet_key

    def _get_spreadsheet(self):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', Sheet.SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))

        return service.spreadsheets()
    
    def _date_format(self, dataframe, datecolumn):
        dataframe['Timestamp'] = dataframe.iloc[:,datecolumn:datecolumn+1].astype('str')
        dataframe['Timestamp'] = dataframe['Timestamp'].apply(parse)
        return dataframe

    def get_data(self):
        # Call the Sheets API
        RANGE_NAME = 'Sheet1!A:C'        
        result = self._get_spreadsheet().values().get(spreadsheetId=self.sheet_key,
                                                range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            raise('No data found.')
        else:
            connection_df = pd.DataFrame(values, columns = ['OriginalTimestamp', 'Device', 'Status'])
            return connection_df

    def get_last_record(self):
        connection_df = self.get_data()[-1:]
        self._date_format(connection_df,0)
        return connection_df.reset_index(drop=True)

        

    


