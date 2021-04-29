# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 00:10:46 2021

@author: Grant Miller
"""

import csv
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot


from ipstack import GeoLookup
#fail2ban.actions


class project:
    def step0 (self):
        with open('interest.csv', 'w', newline='') as file:
            writer1 = csv.writer(file)
            with open('ignore.csv', 'w', newline='') as file:
                writer2 = csv.writer(file)
                for x in range(14):
                    with open('fail2banlogs/fail2ban.log.'+ str(x), newline='') as csvfile:
                        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                        for row in spamreader:
                            m = re.search( 'NOTICE', str(row))
                            if m:
                                writer1.writerow(row)
                            else:
                                writer2.writerow(row)
        
    def step1(self, interest, ignore):
        with open('IPs.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            with open(interest, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spamreader:
                    date = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}',str(row)).group()
                    time = re.search(r'\d{2}[:/]\d{2}[:/]\d{2}', str(row)).group()
                    ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", str(row)).group()
                    inf = [date + " " + time, ip]
                    writer.writerow(inf)
        
    def step2(self):
        print("step2")
        df = pd.read_csv("IPs.csv", names=['date','ip'], header=None)
        print(df)
        # how many unique IPs?
        print(df.nunique())
        # how many of each IP?
        print(df['ip'].value_counts())
        
    def step3(self):
        df = pd.read_csv("IPs.csv", names=['date','ip'], header=None)
        unique = df['ip'].unique()
        # ryan m's API key
        # careful: limited to 10,000 requests
        gl = GeoLookup("ba1b4b735b7c286f04a392635dc6719e")

        cols = ['ip','continent_code','continent_name','country_code','country_name','region_name','city','zip','latitude','longitude']
        tempData = []
        
        for i in unique:
            response = gl.get_location(i)
            locData = []
            for c in cols:
                locData.append(response[c])
            tempData.append(locData)
        td = pd.DataFrame(data=tempData,columns=cols)
        td.to_csv('locs.csv')
        print(td)
        # merge the location data with the IP data, where IPs are the same
        complete = pd.merge(df,td,how='left',on='ip')
        complete.to_csv('complete.csv')
            
        print(complete)
        
    def step4(self):
        print("step4")
        df = pd.read_csv('locs.csv', usecols= ['ip','continent_name','continent_code','country_code','country_name','latitude','longitude'])
        print(df)
        df['size']=pd.Series([131368309 for x in range(len(df.index))],index=df.index)
        fig=go.Figure(data=go.Scattergeo(lon=df['longitude'],lat=df['latitude'],
                                         text=df['ip'],mode='markers', marker_color='purple',
                                         ))
        fig.update_layout(title='IP Adresses')
        plot(fig)
    def step5(self):
        print("step5")
        
        
p = project()
#p.step0()
#p.step1("interest.csv", "ignore.csv")
#p.step2()
#p.step3()
p.step4()