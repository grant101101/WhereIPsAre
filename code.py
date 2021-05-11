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
import plotly.graph_objects as go
from plotly.offline import plot
#fail2ban.actions

pio.renderers.default='browser'

pd.set_option('display.max_columns',None)

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
        df['date']=pd.to_datetime(df['date'])
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
        gl = GeoLookup("f26f5007b5f7a0a3501682919778805c")

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
        country_value_counts=df['country_code'].value_counts()
        valuesdf=pd.DataFrame(country_value_counts)
        valuesdf=valuesdf.reset_index()
        valuesdf.columns=['country_code','code_count']
        df['size']=pd.Series([131368309 for x in range(len(df.index))],index=df.index)
        fig1=go.Figure(data=go.Scattergeo(lon=df['longitude'],lat=df['latitude'],
                                         text=df['ip'],mode='markers', marker_color='purple',
                                         ))
        fig1.update_layout(title='IP Address Locations Across the World')
        #plot(fig1)
        
        #histogram
        fig2=px.histogram(valuesdf,x='country_code',y='code_count',
                          labels={'country_code':'Country Code',
                                  'code_count':'Number of IPs'})
        fig2.update_layout(title='Number of IPs From Each Country')
        #plot(fig2)
        
        countrylat=[35,38,16,64,51,37,-33,22.25,60,43,46,54]
        countrylon=[105,-97,106,26,9,127,-56,114.1667,100,25,2,-2]
        valuesdf['country_lat']=countrylat
        valuesdf['country_lon']=countrylon
        valuesdf['code_count']=valuesdf['code_count']
        #print(valuesdf)
        fig3=px.scatter_geo(valuesdf,lat='country_lat',lon='country_lon',size='code_count',projection='natural earth',title='Bubble Map of IPs')
        #plot(fig3)
        
        fig4=go.Figure(data=[go.Table(
            header=dict(values=['Country Code','Country Count'],
                        fill_color='paleturquoise',align='left'),
            cells=dict(values=[valuesdf['country_code'],valuesdf['code_count']],
                               fill_color='lavender',align='left'))
                               ])
        #plot(fig1)
        #plot(fig2)
        #plot(fig3)
        #plot(fig4)


p = project()
#p.step0()
#p.step1("interest.csv", "ignore.csv")
#p.step2()
#p.step3()
#p.step4("complete.csv")
#p.step5()
