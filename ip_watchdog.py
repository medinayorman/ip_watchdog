
### requeriments libraries
## pip install requests

import requests
from bs4 import BeautifulSoup

import sqlite3
from sqlite3 import Error

#### web ip request
def get_by_webpage():
    URL = 'https://www.cual-es-mi-ip.net'
    page = requests.get(URL)
    
    ## html esta en page.content
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    title_elem2 = soup.find('span', class_='big-text font-arial')
    print(title_elem2.text)
    
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
    
    print(response.json()['query'])
    ##print(response.headers)

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
    sql = ''' INSERT INTO ip_requests(web_request,api_request,api_request_js)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid
def select_last_record__ip_requests(conn):
    cur = conn.cursor()
    cur.execute("SELECT rowid,web_request,api_request_js  FROM ip_requests ORDER BY rowid DESC ")
 
    #rows = cur.fetchall()
    #for row in rows:
    #    #print(row)
    #    print(f'{row[0]} {row[1]} {row[2]}')

    roww = cur.fetchone()
    print(roww)
def create_db():
    database_file = r"./ip_watchdog.db"
    conn = create_connection(database_file)
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS ip_requests (
                                        web_request text NOT NULL,
                                        api_request text,
                                        api_request_js text
                                    ); """

    create_table(conn, sql_create_projects_table)
    with conn:
        firts_print = ('0.0.0.0', '0.0.0.0', '{"json":"here"}')
        project_id = insert_table__ip_requests(conn, firts_print)
        print("was create first print",project_id)
        select_last_record__ip_requests(conn)

def main():

	##initial vars
	database_file = r"./ip_watchdog.db"
	conn = create_connection(database_file)
	

	get_by_webpage()
	get_by_api()

if __name__ == '__main__':
    #main()
    create_db()
