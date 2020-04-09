
### requeriments libraries
## pip install requests==2.23.0
## pip install beautifulsoup4==4.9.0

import requests
from bs4 import BeautifulSoup

import sqlite3
from sqlite3 import Error

from datetime import datetime

from pathlib import Path

import json

import time



#### web ip request
def get_by_webpage():
    URL = 'https://www.cual-es-mi-ip.net'
    page = requests.get(URL)
    
    ## html esta en page.content
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    title_elem2 = soup.find('span', class_='big-text font-arial')
    #print(title_elem2.text)
    return title_elem2.text
    
    ## other way for get ip 
    #title_elem = soup.find_all('span', class_='big-text font-arial')
    #for job_elem in title_elem:
    #    #print(job_elem, end='\n'*2)
    #    print(job_elem.text)

#### API request _ get public ip from API 
def get_by_api():
    
    URL_ip_get = 'https://extreme-ip-lookup.com/json/'
    response = requests.get(URL_ip_get)
    
    #print(response.content)
    #response = requests.get(URL_ip_get,params='',headers={'Content-Type': 'text/html; charset=UTF-8','Content-Encoding': 'br'})
    
    #print(response.json()['query'])
    ##print(response.headers)
    return response.json()

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def check_db_existence():
	print("XD")


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_table__ip_requests(conn, project):
    sql = ''' INSERT INTO ip_requests(web_request,api_request,api_request_js,timestamp)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid

##
def select_last_record__ip_requests(conn):
    cur = conn.cursor()
    cur.execute("SELECT rowid,web_request,api_request,api_request_js,timestamp  FROM ip_requests ORDER BY rowid DESC ")
 
    #rows = cur.fetchall()
    #for row in rows:
    #    #print(row)
    #    print(f'{row[0]} {row[1]} {row[2]} {row[4]}')

    roww = cur.fetchone()
    print(roww)
    
##
def select_last_N_records__ip_requests(conn,n):
    cur = conn.cursor()
    cur.execute("SELECT rowid,web_request,api_request,timestamp  FROM ip_requests ORDER BY rowid DESC LIMIT ?",(n,))
    
    roww = cur.fetchall()
    for record in roww:
        print(record)
    
def create_db():
    database_file = r"./ip_watchdog.db"
    conn = create_connection(database_file)
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS ip_requests (
                                        web_request text NOT NULL,
                                        api_request text,
                                        api_request_js text,
                                        timestamp text
                                    ); """

    create_table(conn, sql_create_projects_table)
    with conn:
        firts_print = ('0.0.0.0', '0.0.0.0', '{"json":"here"}', "2016-01-01 10:20:05.123")
        project_id = insert_table__ip_requests(conn, firts_print)
        print("was create first print",project_id)
        select_last_record__ip_requests(conn)
        print("----------------------")

def main():
    time_for_loop = 420
    exit_loop = 1
    fileName = Path("./ip_watchdog.db")
    if fileName.is_file():
        print ("Database 'ip_watchdog.db' exist")
        database_file = r"./ip_watchdog.db"
        conn = create_connection(database_file)
    else:
        print ("File not exist, the database will be create")
        create_db()
        database_file = r"./ip_watchdog.db"
        conn = create_connection(database_file)
    ##initial vars
    while (exit_loop == 1):
        try:
            evaluation_ip(conn)
        except:
            #exit_loop = 0
            print("Bad request")
        time.sleep(time_for_loop)
    
def evaluation_ip(conn):
    with conn:
        print("---------- Evaluation ------------")
        now = datetime.now()
        s1 = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        record_web = get_by_webpage()
        record_api = get_by_api()
        print("Public IP by_API : ",record_api['query'],"   Public IP by_web : ",record_web)
        record_api_json = json.dumps(record_api) 
        
        record_actual = (record_web, record_api['query'], record_api_json, s1)
        print("id_record :" ,insert_table__ip_requests(conn, record_actual))
        select_last_N_records__ip_requests(conn,10)
    

if __name__ == '__main__':
    main()
    #create_db()
