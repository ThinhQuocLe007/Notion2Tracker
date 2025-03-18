#!/usr/bin/python3
import requests 
import pandas as pd 
import plotly.express as px 
import datetime as dt 
import os 

# Notion APT details
NOTION_API_KEY = '' # your notion apikey 
DATABASE_ID = '' # use database_id
HEADERS = {
    'Authorization': f'Bearer {NOTION_API_KEY}', 
    'Content-Type': 'application/json', 
    'Notion-Version': '2022-06-28'
}

# Clear the output 
def clear_console(): 
    os.system('clear' if os.name == 'posix' else 'cls') 


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



def filter_and_save(data): 
    df = pd.DataFrame(data)
    
    # Filter the month 
    df['Date'] = pd.to_datetime(df['Date']) 
    current_month = dt.datetime.now().month 
    current_year = dt.datetime.now().year

    df_filtered = df[(df['Date'].dt.month == current_month ) & (df['Date'].dt.year == current_year)]
    df_filtered = df_filtered.sort_values(by= 'Date', ascending= True) 

    # save to csv 
    month_map = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
    }

    fix_path = '/home/lequocthinh/Desktop/pythonCode/Project/TRACKER/'
    file_name = f'{month_map[current_month]}_{current_year}.csv'
    file_path = os.path.join(fix_path, file_name)
    df_filtered.to_csv(file_path, index= False)
    print(f'Data saved at: {file_name}')

def main(): 
    # Clean the file.log ( temporary ) 
    file_path = '/home/lequocthinh/cron_test.log' 
    with open(file_path, 'w') as f: 
        f.write("") 
    data = fetch_notion_data() 
    filter_and_save(data) 

if __name__ == '__main__': 
    main()
