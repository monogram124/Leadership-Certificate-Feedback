import sqlite3

import httplib2
from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery

from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def create(self):
        self.conn = sqlite3.connect("telegram_messages.db")
        self.cur = self.conn.cursor()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                name TEXT,
                house TEXT,
                exp TEXT,
                points INTEGER,
                done TEXT,
                skills TEXT,
                repeat TEXT,
                exactly TEXT,
                difficulties TEXT,
                team TEXT,
                motivation TEXT,
                moment TEXT,
                result INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            ''')
        
        self.conn.commit()
        self.conn.close()

    def export_into_sheets(self):
        self.conn = sqlite3.connect("telegram_messages.db")
        self.cur = self.conn.cursor()
        
        CREDENTIALS_FILE = "creds.json"
        spreadsheet_id = os.getenv("SHEETS_ID")
        
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        httpAuth = credentials.authorize(httplib2.Http())
        service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range="A:A"  
        ).execute()

        sheet_data = result.get('values', [])

      
        if len(sheet_data) > 1:
            last_exported_id = int(sheet_data[-1][0])  
        else:
            last_exported_id = 0  

        self.cur.execute("SELECT * FROM messages WHERE id > ?", (last_exported_id,))
        new_rows = self.cur.fetchall() 

        self.conn.close()

        if not new_rows: # в случае если нет чего выгружать
            return
        
        values = []
        for row in new_rows:
            values.append(list(row))  
        
        current_rows = len(sheet_data) 

        body = {
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": f"A{current_rows + 1}",  
                    "majorDimension": "ROWS",
                    "values": values  
                }
            ]
        }

        response = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()

        print(f"{response.get('totalUpdatedCells')} cells updated.")

    def save_message(self, message, user_form):
        self.conn = sqlite3.connect("telegram_messages.db")
        self.cur = self.conn.cursor()

        if user_form[message.chat.id]["points"] == "5":
            self.cur.execute('''
                INSERT INTO messages (user_id, username, name, house, exp, points, done, skills, repeat, result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                message.chat.id, 
                message.from_user.first_name,
                user_form[message.chat.id]['name'],
                user_form[message.chat.id]['house'],
                user_form[message.chat.id]['exp'], 
                int(user_form[message.chat.id]['points']),
                user_form[message.chat.id]['done'],
                user_form[message.chat.id]['skills'][0:len(user_form[message.chat.id]['skills']) - 2], 
                user_form[message.chat.id]['repeat'], 
                int(user_form[message.chat.id]['result'])
            ))      

            self.conn.commit()

        elif user_form[message.chat.id]["points"] == "10":
            self.cur.execute('''
                INSERT INTO messages (user_id, username, name, house, exp, points, done, skills, exactly, difficulties, team, result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                message.chat.id, 
                message.from_user.first_name,
                user_form[message.chat.id]['name'], 
                user_form[message.chat.id]['house'], 
                user_form[message.chat.id]['exp'], 
                int(user_form[message.chat.id]['points']), 
                user_form[message.chat.id]['done'], 
                user_form[message.chat.id]['skills'][0:len(user_form[message.chat.id]['skills']) - 2], 
                user_form[message.chat.id]['exactly'], 
                user_form[message.chat.id]['difficulties'], 
                user_form[message.chat.id]['team_work'], 
                int(user_form[message.chat.id]['result'])
            ))
            
            self.conn.commit()

        elif user_form[message.chat.id]["points"] == "15":
            self.cur.execute('''
            INSERT INTO messages (user_id, username, name, house, exp, points, done, skills, exactly, difficulties, team, motivation, moment, result)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                message.chat.id, 
                message.from_user.first_name,
                user_form[message.chat.id]['name'], 
                user_form[message.chat.id]['house'], 
                user_form[message.chat.id]['exp'], 
                int(user_form[message.chat.id]['points']), 
                user_form[message.chat.id]['done'], 
                user_form[message.chat.id]['skills'][0:len(user_form[message.chat.id]['skills']) - 2], 
                user_form[message.chat.id]['exactly'], 
                user_form[message.chat.id]['difficulties'], 
                user_form[message.chat.id]['team_work'], 
                user_form[message.chat.id]['motivation'], 
                user_form[message.chat.id]['moment'], 
                int(user_form[message.chat.id]['result'])
            ))
            
            self.conn.commit()
        
        self.conn.close()