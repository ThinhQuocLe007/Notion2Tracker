#!/usr/bin/python3

# TODO: 
# 1. Create Notion API 
# 2. Fetch data from Notion 
# 3. Preprocess data 
# 4. Save to mysql 
# 5. Set up crontab for automatic running 

# Import lib 
import requests 
import pandas as pd 
import plotly.express as px 
import datetime as dt 
import os 
import mysql.connector 
from mysql.connector import Error
from config import NOTION_API_KEY, DATABASE_ID, MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD

HEADERS = {
    'Authorization': f'Bearer {NOTION_API_KEY}', 
    'Content-Type': 'application/json', 
    'Notion-Version': '2022-06-28'
}


# Fetch data 
def fetch_notion_data(): 
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers= HEADERS)
    data = response.json()
    
    # Check the status 
    today = dt.date.today() 
    formatted_day = today.strftime("%d/%m/%Y")
    print(f'Day: {formatted_day}')
    if response.status_code == 200: 
        print('Fetch data sucesssfully')
    else: 
        print(f'Fetch failed! Status code: {response.status_code}, Error: {response.text}')

    # Clean data 
    records = [] 
    for result in data.get('results',[]): 
        properties = result['properties']
        row = {
            'Name': properties['Name']['title'][0]['text']['content'] if properties['Name']['title'] else None,
            'Date': properties['Date']['date']['start'] if properties['Date']['date'] else None,
            'Progression': properties['Progression']['formula'].get('number') if 'Progression' in properties else None,
            'Formula': properties['Formula']['formula'].get('number') if 'Formula' in properties else None,
            'DATA_TIME': properties['DATA_TIME']['number'] if 'DATA_TIME' in properties else None,
            'ENGLISH_TIME': properties['ENGLISH_TIME']['number'] if 'ENGLISH_TIME' in properties else None,
            'OTHER_TIME': properties['OTHER_TIME']['number'] if 'OTHER_TIME' in properties else None,
            'RELAX_TIME': properties['RELAX_TIME']['number'] if 'RELAX_TIME' in properties else None,
            'Walking': properties['Walking']['number'] if 'Walking' in properties else None,
            'NoFap': properties['NoFap']['checkbox'] if 'NoFap' in properties else False
        }
        records.append(row)
    return records

# Establish a connection
def save2mysql(data):  
    try:
        connection = mysql.connector.connect(
            host= MYSQL_HOST, 
            database = MYSQL_DATABASE,
            user= MYSQL_USER, 
            password= MYSQL_PASSWORD
        )
        if connection.is_connected(): 
            cursor = connection.cursor() 

            # create table if not exist 
            create_table_query = """
            create table if not exists notion_data(
                id int auto_increment primary key, 
                Name varchar(255), 
                Date DATE, 
                Progression FLOAT, 
                Formula FLOAT, 
                DATA_TIME FLOAT, 
                ENGLISH_TIME FLOAT, 
                OTHER_TIME FLOAT, 
                RELAX_TIME FLOAT, 
                Walking FLOAT, 
                NoFap BOOLEAN 
            ); 
            """
            cursor.execute(create_table_query) 
            # Insert data into the table 
            insert_query = """
            insert into notion_data (Name, Date,Progression,Formula, DATA_TIME, ENGLISH_TIME, OTHER_TIME, RELAX_TIME, Walking, NoFap)
            values (%s, %s, %s,%s,%s, %s, %s, %s, %s, %s) ; 
            """
            for record in data: 
                cursor.execute(insert_query, (
                    record['Name'], 
                    record['Date'],
                    record['Progression'], 
                    record['Formula'], 
                    record['DATA_TIME'], 
                    record['ENGLISH_TIME'], 
                    record['OTHER_TIME'], 
                    record['RELAX_TIME'], 
                    record['Walking'],
                    record['NoFap']
                )) 
            
            connection.commit() 
            print('Data saved to mysql sucessfully')
    except Error as e: 
        print(f'Error: {e}')

    finally: 
        if connection.is_connected(): 
            cursor.close() 
            connection.close() 
            print('Mysql connection is closed')


def main(): 
    # Clean the file.log ( temporary ) 
    file_path = '/home/lequocthinh/cron_test.log' 
    with open(file_path, 'w') as f: 
        f.write("") 
    
    # Fetch and Save data 
    data = fetch_notion_data() 
    if data: 
        save2mysql(data) 

if __name__ == '__main__': 
    main()
