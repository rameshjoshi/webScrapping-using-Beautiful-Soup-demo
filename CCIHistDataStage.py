__author__ = 'rjoshi'
# ****************************************************/
# Filename: CCIHistDataStage.py
# Created: Ramesh Joshi
# Purpose: Dump CCI data into staging table
# Change history:
# 09.14.2015  / Ramesh Joshi
#             /
# ****************************************************/

import os
import csv
import re
import pyodbc



# database connection

cnxn = pyodbc.connect('DSN=projectio_dsn')
cursor = cnxn.cursor()

# read files from the folder

for root, dirs, files in os.walk(os.path.abspath(r"C:\Users\rjoshi\Dropbox (The Gordian Group)\Project Io\Sprint 8\Technology\SortedDataforDB")):
  for file in files:
    #print (os.path.join(root, file))
    file_read = open(os.path.join(root, file))
    for row in csv.reader (file_read):
        #print (row)

        price = row[4]
        if price is None or price == "":
            price= 0

        try:
            float(price)
        except ValueError:
            price = 0

        #state=re.search(r'(?<=:)\w+',row[0] ).group(0)
        #city = re.search(r'(?<=:)\w+',row[1] ).group(0)
        #matCode = re.search(r'(?<=:)\w+',row[0] ).group(0)

        state = re.split(":",row[0])

        state=state[1]

        if state is None or state == "":
            state = " "

        city = re.split(":", row[1])
        city = city[1]

        if city is None or city == "":
            city = " "

        cityCode = re.split(":", row[2])
        cityCode = cityCode[1]

        if cityCode is None or cityCode == "":
            cityCode = " "

        try:
            MaterialCode = re.split(":", row[3])
            MaterialCode = MaterialCode[0]
        except IndexError:
            MaterialCode = " "

        try:

            Supplier = re.split(":", row[3])
            Supplier = Supplier[1]
        except IndexError:
            Supplier = " "



        insert_stmt_sql = 'insert into dbo.CCIHistoricalDataStaging \
                             ([file_name], [state],[city], [citycode], [MaterialCode],[Supplier], [price]  ) ' \
                                   'values ( ' + " '" + file_read.name + "' ,'" + state + "' ,'" + city + "' ,'" + cityCode + "' ,'" + MaterialCode  + "' ,'" + Supplier + "' ," + str(price)+")"

        cursor.execute(insert_stmt_sql)


cnxn.commit()
cnxn.close()
