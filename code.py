#%%
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 11:50:50 2021

@author: kiddra
"""
import csv
import re
import pandas as pd
import plotly as pl
from ipstack import GeoLookup
import plotly.express as px
import plotly.io as pio
#fail2ban.actions

pio.renderers.default='browser'

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
                            m = re.search( 'Ban', str(row))
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
                    ip = re.search(r"\d{1,3}[./]\d{1,3}[./]\d{1,3}[./]\d{1,3}", str(row)).group()
                    inf = [date + " " + time, ip]
                    writer.writerow(inf)
        
    def step2(self):
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

        cols = ['ip','continent_code','continent_name','country_name','country_code','latitude','longitude']
        tempData = []

        for i in unique:
            response = gl.get_location(i)
            locData = []
            for c in cols:
                locData.append(response[c])
            tempData.append(locData)
            
        td = pd.DataFrame(data=tempData,columns=cols)
        td.to_csv('locs.csv')
        
        # merge the location data with the IP data, where IPs are the same
        complete = pd.merge(df,td,how='left',on='ip')
        complete.to_csv('complete.csv')
            
        print(complete)

    def step4(self, complete):
        data = pd.read_csv(complete, names=['date','ip','continent_code','continent_name','country_name','country_code','latitude','longitude'], header=None)
        ips = data['ip'].value_counts()
        continents = data.groupby(['continent_name','ip']).groups
        countries = data.groupby('country_name').groups
        
    def step5(self):
        print("step5")
        df = pd.read_csv('complete.csv', names=['date','ip','continent_code','continent_name','country_name','country_code','latitude','longitude'], header=0)
        print(df.to_string)
        
        # IPs by hour
        df['date'] = df['date'].str.split(':').str[0]
        data = df.sort_values(by='date')
        china = data.loc[data['country_code']=='CN']
        
        fig = px.histogram(data,x='date',title="IPs Banned, by Time of Day",labels={'date':'Hour of Day','count':'Count'})
        #fig.show()
        
        
p = project()
p.step0()
p.step1("interest.csv", "ignore.csv")
p.step2()
p.step3()
p.step4("complete.csv")
p.step5()