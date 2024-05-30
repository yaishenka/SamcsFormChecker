from oauth2client.service_account import ServiceAccountCredentials
import gspread
from settings import account_credentials_file, requests_per_minute
import string
import datetime
import time
import math

class GoogleSheetsReader:
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(account_credentials_file, scope)
    gc = gspread.authorize(credentials)
    alphabet = string.ascii_uppercase
    time_of_last_call = datetime.datetime.fromtimestamp(0)
    throttle_period = datetime.timedelta(
        seconds=60 / requests_per_minute, minutes=0, hours=0
    )

    @staticmethod
    def throttle():
        now = datetime.datetime.now()
        time_since_last_call = now - GoogleSheetsReader.time_of_last_call
        if time_since_last_call > GoogleSheetsReader.throttle_period:
            GoogleSheetsReader.time_of_last_call = now
        time.sleep(math.ceil(60 / requests_per_minute))

    @staticmethod
    def get_all_records(table_url: str, sheet=0):
        GoogleSheetsReader.throttle()
        table = GoogleSheetsReader.gc.open_by_url(table_url)
        worksheet = table.get_worksheet(sheet)
        return worksheet.get_all_records()

    @staticmethod
    def get_all_values(table_url: str, sheet=0):
        GoogleSheetsReader.throttle()
        table = GoogleSheetsReader.gc.open_by_url(table_url)
        worksheet = table.get_worksheet(sheet)
        return worksheet.get_all_values()

    @staticmethod
    def get_worksheet(table_url: str, sheet=0):
        GoogleSheetsReader.throttle()
        table = GoogleSheetsReader.gc.open_by_url(table_url)
        worksheet = table.get_worksheet(sheet)
        return worksheet

    @staticmethod
    def create_and_return_worksheet(table_url: str, sheet_title: str, rows: str, cols: str):
        GoogleSheetsReader.throttle()
        table = GoogleSheetsReader.gc.open_by_url(table_url)
        try:
            worksheet = table.worksheet(sheet_title)
            return worksheet
        except:
            pass
        worksheet = table.add_worksheet(title=sheet_title, rows=rows, cols=cols)
        return worksheet

    @staticmethod
    def create_header(worksheet, header):
        header_len = len(header)
        begin = f'{GoogleSheetsReader.alphabet[0]}1'
        end = f'{GoogleSheetsReader.alphabet[header_len - 1]}1'
        cells_list = worksheet.range(f'{begin}:{end}')
        for i, cell in enumerate(cells_list):
            cell.value = str(header[i])
        GoogleSheetsReader.throttle()
        worksheet.update_cells(cells_list)
