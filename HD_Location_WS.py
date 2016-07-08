__author__ = 'rjoshi'
# ****************************************************/
# Filename: HD_Location_WS.py
# Created: Ramesh Joshi
# Purpose: Web Scrape HD store locations data
# Change history:
# 09.16.2015  / Ramesh Joshi
#             /
# **********************************************************

from bs4 import BeautifulSoup
import requests
import re, cgi
import pyodbc

url_string = "http://localad.homedepot.com/HomeDepot/Entry/Locations/"
cnxn = pyodbc.connect('DSN=projectio_dsn')
cursor = cnxn.cursor()

r = requests.get(url_string)
soup = BeautifulSoup(r.content, "html.parser")
# print (soup.prettify())
#for stateHeader_div in soup.findAll("div", {"class": "stateHeader"})[1:]:  # Strip the last element from the list
#    State = stateHeader_div.text
    # print(State)

for locationsLink_div in soup.find_all("a", {"class": "locationsLink"})[1:]:
    r = requests.get(
            "http://www.homedepot.com/webapp/wcs/stores/servlet/THDStoreFinderStoreSet?recordId=" + re.search(
                r'(?<=storeid=)\w+', locationsLink_div['data-tracking-redirectlink']).group(
                0) + "&storeFinderCartFlow=false")
    # print (State)
    # print (locationsLink_div.attrs)
    # print (locationsLink_div['data-tracking-redirectlink'])
    store_id = re.search(r'(?<=storeid=)\w+', locationsLink_div['data-tracking-redirectlink']).group(0)
    Address = locationsLink_div.text
    set_store_url = "http://www.homedepot.com/webapp/wcs/stores/servlet/THDStoreFinderStoreSet?recordId=" + re.search(
            r'(?<=storeid=)\w+', locationsLink_div['data-tracking-redirectlink']).group(
            0) + "&storeFinderCartFlow=false"
    set_store_redirect_url = r.url
    # print ( re.search(r'(?<=storeid=)\w+',locationsLink_div['data-tracking-redirectlink'] ).group(0), locationsLink_div.text)
    # print (locationsLink_div.text)
    # print ("http://www.homedepot.com/webapp/wcs/stores/servlet/THDStoreFinderStoreSet?recordId=" +  re.search(r'(?<=storeid=)\w+',locationsLink_div['data-tracking-redirectlink'] ).group(0) +"&storeFinderCartFlow=false")
    # Print ("http://www.homedepot.com/webapp/wcs/stores/servlet/StoreFinderViewDetails?storeZip=29483&langId=-1&latitude=33.030723&storeCity=Summerville&recordId=1120&longitude=-80.161433&storeState=SC&catalogId=10053&storeFinderCartFlow=false&storeId=10051&ddkey=http:THDStoreFinderStoreSet
    # print(r.url)
    # print (r)
    cursor.execute(
            """insert into dbo.tbl_HD_Store_location_web_scrape ( store_id  ,Address ,set_store_url ,set_store_redirect_url ) values (?,?,?,? )""",
            store_id, Address, set_store_url, set_store_redirect_url)
    cnxn.commit()

