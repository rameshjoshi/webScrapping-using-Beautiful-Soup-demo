__author__ = 'rjoshi'
# ****************************************************/
# Filename: cincinatti_RMC.py
# Created: Ramesh Joshi
# Purpose: Extract price from cincinattireadymix.xom
# Change history:
# 05.06.2015  / Ramesh Joshi
#             /
# ****************************************************/

from bs4 import BeautifulSoup
import requests
import re
import pyodbc
# import urllib2
# import urllib2

#r = requests.get("http://www.yellowpages.com/search?search_terms=Concrete+supplier&geo_location_terms=Boston%2C+MA")
r = requests.get("http://www.cincinnatireadymix.com/concrete_prices.htm")
soup = BeautifulSoup ( r.content, "html.parser")

#print (soup.prettify())

#print (soup.find(string=re.compile("3500")))

insert_stmt_sql = 'insert into dbo.tbl_web_scrape (source, value) values ( ' + "'" + 'http://www.cincinnatireadymix.com/concrete_prices.htm' + "' ,'" + soup.find(string=re.compile("3000")).strip() + "')"
#print (insert_stmt_sql)

#for data in soup.find(string=re.compile("per cubic yard")):
    #print(data)

#for link in soup.find_all('per cubic yard'):
    #print (link.get("href"))
    #print (link)
    #for data in link:
     #   print ( data.per cubic yard)

cnxn = pyodbc.connect('DSN=projectio_dsn')

cursor = cnxn.cursor()

cursor.execute(insert_stmt_sql)
cnxn.commit()

#cursor.execute("SELECT  [Description]  ,[MaterialCode]  ,[City]  ,[recent_price]  ,[last_price] ,[trend], [dollar_diff] ,[percent_diff]  ,[quarter] from  dbo.tbl_price_alert_data_recent_qtr ")
#row = cursor.fetchone()
#for row in cursor:
 #   print (row)
#if row:
    #print (row)


