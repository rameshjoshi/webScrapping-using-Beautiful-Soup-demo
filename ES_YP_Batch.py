# ****************************************************/
# Filename: ES_YP_Batch.py
# Created: Ramesh Joshi
# Purpose: Extract electrical supplier info from Yellow page
# Change history:
# 08.06.2015  / Ramesh Joshi
#             /
# ****************************************************/

__author__ = 'rjoshi'
from bs4 import BeautifulSoup
import requests
import re, cgi

import pyodbc
# import urllib2
# import urllib2



regex = re.compile(r'>([\w\.-]+)</a></td>')

tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

BusinesslistInt = 0

CCIUSlocationSelect = "SELECT [City]      ,[Abbreviation]  FROM [dbo].[tblCCILocation] where [Abbreviation] != 'CN' order by city desc"

cnxn = pyodbc.connect('DSN=projectio_devsql')
#cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=RJoshi1314;DATABASE=project_io;Trusted_Connection=yes')


cursor = cnxn.cursor()

cursor.execute(CCIUSlocationSelect)
rows = cursor.fetchall()
for row in rows:
# print (row[0])
  if row:
    print(row)
    BusinesslistInt = 0
    print(row[1])
    url_string = "http://www.yellowpages.com/search?search_terms=electrical+supplier&geo_location_terms=" + row[0] + "%2C+" + row[1]
    print(url_string)
    # build the url_string
    r = requests.get(url_string)
    soup = BeautifulSoup(r.content, "html.parser")
    for main_div in soup.findAll("div", {"class": "info"})[0:-1]:  # Strip the last element from the list
      # print(main_div)
      business_name = main_div.a.text
      if business_name is None:
          business_name = 'none'
      print("business name:" + business_name)
      for street_address in main_div.findAll("span", {"itemprop": "streetAddress"}):
        street_address = street_address.text  # main_div.div.p.span.text
        if street_address is None:
            street_address = 'none'
        print("Street Adress :" + street_address)
        for city in main_div.findAll("span", {"itemprop": "addressLocality"}):
          city = city.text
          if city is None:
            city = 'none'
          print("city  :", city)
        for postal_code in main_div.findAll("span", {"itemprop": "postalCode"}):
          postal_code = postal_code.text
          if postal_code is None:
              postal_code = 'none'
          print("Postal Code :", postal_code)
          # print(main_div.findAll ("div", {"class":"phones phone primary"}))
        for phone in main_div.findAll("div", {"class": "phones phone primary"}):
          phone = phone.text
          if phone is None:
              phone = 'none'
          # print("Phone :" + phone.text)
        for url in main_div.findAll("a", {"class": "track-visit-website"}):
          BusinesslistInt = BusinesslistInt + 1
          url = url['href']
          if url is None:
              url = 'none'
          print("url: " + url)
          # insert the result in db table
          insert_stmt_sql = 'insert into dbo.tbl_ElectricalSupplierlist_web_scrape \
                             ([source]      ,[city]      ,[State]      ,[list_no]      ,[business_name]      ,[Street_address]      ,[web_city]      ,[Postal_code]      ,[phone]      ,[business_url]) ' \
                                   'values ( ' + " '" + url_string + "' ,'" + row[0] + "' ,'" + row[1] + "' ,'" + str(BusinesslistInt) + "' ,'" + business_name + \
                                   "' ,'" + street_address + "' ,'" + city + "' ,'" + postal_code + "' ,'" + phone + "' ,'" + url + "')"
          print(insert_stmt_sql)
          #cursor.execute('SET NOCOUNT ON')
          #cursor.execute ("""insert into dbo.tbl_ElectricalSupplierlist_web_scrape(source,city, State,list_no, business_name,Street_address,web_city,Postal_code,phone, business_url ) values (?,?,?,?,?,?,?,?,?,? )""",url_string,row[0],row[1],BusinesslistInt,business_name,street_address,city,postal_code,phone,url)
          cursor.execute ("""insert into dbo.tbl_ElectricalSupplierlist_web_scrape(source,city, State,list_no, business_name,Street_address,web_city,Postal_code,phone, business_url ) values (?,?,?,?,?,?,?,?,?,? )""",url_string,row[0],row[1],BusinesslistInt,business_name,street_address,city,postal_code,phone,url)


          #cursor.execute('SET NOCOUNT ON')
          #rowcount = cursor.execute(insert_stmt_sql).rowcount
          #print("rowcount -----------" + str(rowcount))
          #if rowcount != 1:
          #    break
cnxn.commit()
