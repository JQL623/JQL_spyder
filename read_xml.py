#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 15:55:36 2020
@author: JQL_2020_4_15
"""

from bs4 import BeautifulSoup as soup
import pandas as pd

xml_files = ['EGI_Net_64_Placement','Quik_Cap_Net_64']
for xml_file_name in xml_files:
    xml_file_name_full = '/Users/jq/JQL_spyder/Scrape_Data/' + xml_file_name + '.xml'
    my_file = open(xml_file_name_full,'r')
    my_contents = my_file.read()
    data = soup(my_contents,'xml')
    parse_field = ['Label','XCoordinate','YCoordinate']

    label_x_y = {}
    for ff in parse_field:
        data_text = data.find_all(ff)
        my_data = []
        for i in data_text:
            my_data.append(i.get_text())
        d = {ff:my_data}
        label_x_y.update(d)
    label_x_y_df = pd.DataFrame(data=label_x_y)
    if xml_file_name == 'EGI_Net_64_Placement':
        label_x_y_df_final = label_x_y_df.drop([64])
    label_x_y_df_final.to_csv(xml_file_name + '.csv')












my_label = data.findAll('Label')
my_x = data.findAll('XCoordinate')
my_y = data.findAll('YCoordinate')

label_data=[]
for i in my_label:
    label_data.append(i.get_text())
#list(label_data)
#### change last num of int to 100, later change back
#label_data1 = list(map(int,label_data))

x_data=[]
for j in my_x:
    x_data.append(j.get_text())
#list(x_data)
#x_data1 = list(map(float,x_data))

y_data=[]
for z in my_y:
    y_data.append(z.get_text())
#list(y_data)
#y_data1 = list(map(float,y_data))
###str2num

#EGI64data= pd.DataFrame({'Label':label_data1,'XCoordinate':x_data1,'YCoordinate':y_data1},columns=['Label','XCoordinate','YCoordinate'])

#import joblib
#joblib.dump(EGI64data,'EGI_NET_64_Placement.csv')
#combile_lists=list(zip(label_data,x_data,y_data))

