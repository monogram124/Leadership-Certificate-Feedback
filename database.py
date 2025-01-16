import mysql.connector

from datetime import datetime
import pytz

import httplib2
from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery

from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    # TODO: сделать закрытие 
    def connect(self):
        try:
            self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=os.getenv("PASS"),
            port="3306",
            database="lcfdatabase"
            )
            
            print("Подключение к базе данных успешно!")
            
            return self.conn
        except mysql.connector.Error as err:
            print(f"Ошибка подключения: {err}")
            
            return None

    def close(self):
        try:
            self.conn.close()

            print("Соединение с базой данных закрыто!")

        except mysql.connector.Error as err:
            print(f"Ошибка закрытия соединения: {err}")
            
            return None
        
    def create(self):
        try:
            with self.conn.cursor() as cur:
            
                cur.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    username VARCHAR(255),
                    name VARCHAR(255),
                    house VARCHAR(255),
                    exp VARCHAR(255),
                    points INT,
                    done VARCHAR(255),
                    skills VARCHAR(510),
                    `repeat` VARCHAR(255),
                    exactly VARCHAR(255),
                    difficulties VARCHAR(255),
                    team VARCHAR(255),
                    motivation VARCHAR(255),
                    moment VARCHAR(255),
                    result INT,
                    timestamp VARCHAR(255)
                );
                ''')
        except mysql.connector.Error as err:
            print(f"Ошибка создания таблицы: {err}")
       
    def export_into_sheets(self):
        try:
            with self.conn.cursor() as cur:
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

                
                cur.execute("SELECT * FROM messages WHERE id > %s", (last_exported_id,))
                new_rows = cur.fetchall()

                if not new_rows:
                    print("Нет новых данных для выгрузки.")

                    return

                values = [list(row) for row in new_rows]

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

                # print(f"{response.get('totalUpdatedCells')} cells updated.")

                if not os.path.exists(CREDENTIALS_FILE):
                    raise FileNotFoundError("Файл учетных данных не найден.")
        except Exception as e:
            print(f"Ошибка в экспорте данных: {e}")

    def save_message(self, message, user_form):
        try:
            with self.conn.cursor() as cur:

                self.moscow_tz = pytz.timezone("Europe/Moscow")
                self.timestamp = datetime.now(self.moscow_tz).strftime("%d-%m-%Y %H:%M:%S")

                res_skills = ""
                
                for char in str(user_form[message.chat.id]['skills']):
                    if char != "'" and char != "[" and char != "]":
                        res_skills += char
                        
                user_form[message.chat.id]['skills'] = str(user_form[message.chat.id]['skills'])

                if user_form[message.chat.id]["points"] == "5":
                    cur.execute('''
                        INSERT INTO messages (user_id, username, name, house, exp, points, done, skills, `repeat`, result, timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        message.chat.id, 
                        message.from_user.first_name,
                        user_form[message.chat.id]['name'],
                        user_form[message.chat.id]['house'],
                        user_form[message.chat.id]['exp'], 
                        int(user_form[message.chat.id]['points']),
                        user_form[message.chat.id]['done'],
                        res_skills, 
                        user_form[message.chat.id]['repeat'], 
                        int(user_form[message.chat.id]['result']),
                        self.timestamp
                    ))     

                    self.conn.commit() 

                elif user_form[message.chat.id]["points"] == "10":
                    cur.execute('''
                        INSERT INTO messages (user_id, username, name, house, exp, points, done, skills, exactly, difficulties, team, result, timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        message.chat.id, 
                        message.from_user.first_name,
                        user_form[message.chat.id]['name'], 
                        user_form[message.chat.id]['house'], 
                        user_form[message.chat.id]['exp'], 
                        int(user_form[message.chat.id]['points']), 
                        user_form[message.chat.id]['done'], 
                        res_skills, 
                        user_form[message.chat.id]['exactly'], 
                        user_form[message.chat.id]['difficulties'], 
                        user_form[message.chat.id]['team_work'], 
                        int(user_form[message.chat.id]['result']),
                        self.timestamp
                    ))

                    self.conn.commit() 

                elif user_form[message.chat.id]["points"] == "15":
                    cur.execute('''
                    INSERT INTO messages (user_id, username, name, house, exp, points, done, skills, exactly, difficulties, team, motivation, moment, result, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        message.chat.id, 
                        message.from_user.first_name,
                        user_form[message.chat.id]['name'], 
                        user_form[message.chat.id]['house'], 
                        user_form[message.chat.id]['exp'], 
                        int(user_form[message.chat.id]['points']), 
                        user_form[message.chat.id]['done'], 
                        res_skills, 
                        user_form[message.chat.id]['exactly'], 
                        user_form[message.chat.id]['difficulties'], 
                        user_form[message.chat.id]['team_work'], 
                        user_form[message.chat.id]['motivation'], 
                        user_form[message.chat.id]['moment'], 
                        int(user_form[message.chat.id]['result']),
                        self.timestamp
                    ))
                    
                    self.conn.commit() 
        except mysql.connector.Error as err:
            print(f"Ошибка сохранения сообщения: {err}")