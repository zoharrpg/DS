import os
from requests import get
import json
import csv
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Task(object):
    def __init__(self):
        self.response = get('http://db.cs.pitt.edu/courses/cs1656/data/hours.json', verify=False) 
        self.hours = json.loads(self.response.content) 

    def part4(self):
        #write output to hours.csv
        filename="hours.csv"
        with open (filename,"w") as csvfile:
            
            csvwriter=csv.writer(csvfile)
            csvwriter.writerow(["name","day","time"])
            
            for line in self.hours:
                csvwriter.writerow([line["name"],line["day"],line["time"]])


    def part5(self):
        #write output to 'part5.txt'
        f = open('part5.txt', 'w') 
        with open("hours.csv") as csvfile:
            reader=csv.reader(csvfile)

            for row in reader:
              print(*row,sep=",",file=f)
              
            
            
            f.close()
        

    def part6(self):
        #write output to 'part6.txt'
        f = open('part6.txt', 'w')
        with open("hours.csv") as csvfile:
            reader=csv.reader(csvfile)

            for row in reader:
              f.write(str(row))
             
              
            
            
            f.close()

     
        

    def part7(self):
        #write output to 'part7.txt'
        f = open('part7.txt', 'w')
        with open("hours.csv") as csvfile:
            reader=csv.reader(csvfile)

            for row in reader:
                for string in row:
                    f.write(string)
             
              
            
            
            f.close()

        


if __name__ == '__main__':
    task = Task()
    task.part4()
    task.part5()
    task.part6()
    task.part7()