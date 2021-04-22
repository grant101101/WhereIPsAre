# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 11:50:50 2021

@author: kiddra
"""
import csv
import re
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
        
    def step2(self, interest, ignore):
        print("step2")
        
    def step3(self):
        print("step3")
        
    def step4(self):
        print("step4")
        
    def step5(self):
        print("step5")
        
p = project()
p.step1("interest.csv", "ignore.csv")