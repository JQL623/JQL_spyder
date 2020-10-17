import requests
from bs4 import BeautifulSoup as soup

my_url = 'https://finance.yahoo.com/quote/%5EDJI?p=^DJI'
m_http = requests.get(my_url)
m_soup = soup(m_http.content,'html.parser')

#m_target = m_soup.find('div',class_='My(6px) Pos(r) smartphone_Mt(6px)').find('span')
m_target = m_soup.find('div',class_='My(6px) Pos(r) smartphone_Mt(6px)').find('div')
m_goal = m_target.getText()
print(m_goal)