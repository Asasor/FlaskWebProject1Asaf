"""
Used structures and classes
"""
from os import path
import json
import pandas as pd
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def create_DataSheetsServiceRoutines():
    return DataSheetsServiceRoutines()

class DataSheetsServiceRoutines(object):
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds']
        client_data = path.join(path.dirname(__file__), '..\\static\\Data\\client_data.json')
        credentials = ServiceAccountCredentials.from_json_keyfile_name(client_data, scope)
        self.client = gspread.authorize(credentials)
        self.ScoutingDataFile = path.join(path.dirname(__file__), '..\\static\\Data\\ScoutingData.csv')

# -------------------------------------------------------
# Get csv of given google sheets by id
# -------------------------------------------------------
    def ReadCSVSheetsDB(self, DocId, num):
        spreadsheet = self.client.open_by_key(DocId)
        with open(self.ScoutingDataFile, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerows(spreadsheet.worksheets()[num].get_all_values())
        df = pd.read_csv(self.ScoutingDataFile)
        return df