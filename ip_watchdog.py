import requests
from bs4 import BeautifulSoup

URL = 'https://www.cual-es-mi-ip.net'
page = requests.get(URL)

## html esta en page.content

soup = BeautifulSoup(page.content, 'html.parser')

title_elem = soup.find_all('span', class_='big-text font-arial')

title_elem2 = soup.find('span', class_='big-text font-arial')
print(title_elem2.text)
for job_elem in title_elem:
    #print(job_elem, end='\n'*2)
    print(job_elem.text)
          
          
URL_ip_get = 'https://api.myip.com'
response = requests.get(URL_ip_get)

print(response.content)

response = requests.get(URL_ip_get,params='',headers={'Content-Type': 'text/html; charset=UTF-8','Content-Encoding': 'br'})

print(response.json())
print(response.headers)


