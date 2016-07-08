__author__ = 'rjoshi'
from bs4 import BeautifulSoup
import requests
import re, cgi

import pyodbc
# import urllib2
# import urllib2

r = requests.get("http://www.yellowpages.com/search?search_terms=Concrete+supplier&geo_location_terms=Boston%2C+MA")
#r = requests.get("http://www.yellowpages.ca/search/si/1/concrete%20supplier/Toronto")
# r = requests.get("http://www.cincinnatireadymix.com/concrete_prices.htm")
soup = BeautifulSoup(r.content, "html.parser")

# print (soup.prettify())

regex = re.compile(r'>([\w\.-]+)</a></td>')

tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

BusinesslistInt = 1


CCIUSlocationSelect = "SELECT [City]      ,[Abbreviation]  FROM [dbo].[tblCCILocation] where [Abbreviation] != 'CN'"

cnxn = pyodbc.connect('DSN=projectio_dsn')

cursor = cnxn.cursor()

cursor.execute(CCIUSlocationSelect)
row = cursor.fetchone()
for row in cursor:
    print (row[0])
    if row:
        print (row[1])
        url_string="http://www.yellowpages.com/search?search_terms=Concrete+supplier&geo_location_terms="+row[0]+"%2C+"+row[1]
        print (url_string)

cnxn.commit()


for main_div in soup.findAll("div", {"class": "info"})[0:-1]: # Strip the last element from the list
    #print(main_div)
    business_name = main_div.a.text
    print("business name:" + business_name)
    for street_address in main_div.findAll("span",{"itemprop":"streetAddress"}):
        street_address =  street_address.text #main_div.div.p.span.text
        print("Street Adress :" + street_address)
    for city in main_div.findAll("span", {"itemprop":"addressLocality"}):
         city = city.text
         print ("city  :", city)
    for postal_code in main_div.findAll("span", {"itemprop":"postalCode"}):
         postal_code = postal_code.text
         print ("Postal Code :", postal_code)
    # print(main_div.findAll ("div", {"class":"phones phone primary"}))
    for phone in main_div.findAll("div", {"class": "phones phone primary"}):
        print("Phone :" + phone.text)
    for url in main_div.findAll("a", {"class": "track-visit-website"}):
        print("url: " + url['href'])
        # phone = main_div.div.text

        # print ( "Phone :" + phone[0])
        # Remove well-formed tags, fixing mistakes by legitimate users
        # no_tags = tag_re.sub('', main_div)
        # Clean up anything else by escaping
        # ready_for_web = cgi.escape(no_tags)
        # Delete any remaining brackets
        # ready_for_web = re.sub('[<>]', '', no_tags)
        # print (no_tags)

# print ( soup.html.body.div)

# print ( soup.html.body.div.nextSibling)


# for all_div in soup.html.body:
# print (all_div)

# for businessName in  soup.find_all(class_=re.compile("business-name")):
# print (businessName)

# for adr in soup.find_all('p', class_="adr"):
# print (adr)

# for info in soup.find_all('div',class_="info"):
# print (info)

# print (soup.find(string=re.compile("3500")))

# insert_stmt_sql = 'insert into dbo.tbl_web_scrape (source, value) values ( ' + "'" + 'http://www.cincinnatireadymix.com/concrete_prices.htm' + "' ,'" + soup.find(string=re.compile("3000")).strip() + "')"
# print (insert_stmt_sql)

# for data in soup.find(string=re.compile("per cubic yard")):
# print(data)

# for link in soup.find_all('per cubic yard'):
# print (link.get("href"))
# print (link)
# for data in link:
#   print ( data.per cubic yard)

 #cnxn = pyodbc.connect('DSN=projectio_dsn')

 #cursor = cnxn.cursor()

 #cursor.execute(insert_stmt_sql)
 #cnxn.commit()

# cursor.execute("SELECT  [Description]  ,[MaterialCode]  ,[City]  ,[recent_price]  ,[last_price] ,[trend], [dollar_diff] ,[percent_diff]  ,[quarter] from  dbo.tbl_price_alert_data_recent_qtr ")
# row = cursor.fetchone()
# for row in cursor:
#   print (row)
# if row:
# print (row)
