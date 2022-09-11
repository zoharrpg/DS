import sqlite3 as lite
import csv
import re
import pandas as pd
import argparse
import collections
import json
import glob
import math
import os
import requests
import string
import sqlite3
import sys
import time
import xml


class Movie_db(object):
    def __init__(self, db_name):
        #db_name: "cs1656-public.db"
        self.con = lite.connect(db_name)
        self.cur = self.con.cursor()
    
    #q0 is an example 
    def q0(self):
        query = '''SELECT COUNT(*) FROM Actors'''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q1(self):
        query = '''
       Select view1.fname,view2.lname
        from list as view1 INNER Join list as view2
        on view1.aid=view2.aid
        where view1.year between 1980 AND 1990 AND view2.year >=2000;
        
        
       
       
       
       
       
            
        '''
        query2 = '''
             Create view if NOT exists List as 
             select * 
             from Actors as a, "Cast" as c, Movies as m
             where a.aid=c.aid AND m.mid=c.mid
               '''
        self.cur.execute(query2)
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
        

    def q2(self):
        query = '''
        select Movies.title, Movies.year 
        from Movies, (select * from Movies where title = "Rogue One: A Star Wars Story") as x   
        where Movies.year= x.year AND Movies.rank > x.rank
        order by Movies.title
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q3(self):
        query = '''
       select a.fname,a.lname,count(x.mid) as count 
       from(
        select DISTINCT aid,mid
        from "Cast" as c
        ) as x,Actors as a,Movies as m
        where x.aid=a.aid AND m.mid=x.mid AND m.title like '%Star Wars%'
        group by x.aid
        order by count desc,lname,fname
        
            
        '''

        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows


    def q4(self):
        query = '''
        select fname,lname
        from Actors as a
        Where a.aid not in 
        (
        select c.aid
        from Actors as a, Movies as m, "Cast" as c
        where a.aid=c.aid AND M.mid=c.mid AND  m.year>=1980
        ) And a.aid in 
        (
        select c.aid
        from Actors as a, Movies as m, "Cast" as c
        
        where a.aid=c.aid AND M.mid=c.mid AND m.year<1980
        ) 
        order by lname,fname
        
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q5(self):
        query = '''
        SELECT fname,lname, count(md.mid) as count
        From Directors as d, Movie_Director as md
        WHERE d.did=md.did
        group by d.did
        order by count desc,lname,fname
        limit 10
         
        
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q6(self):
        query = '''
        Select m.title, count( c.aid) as count
        from Movies as m,"Cast" as c
        where m.mid=c.mid
        group by m.title
        having count>=
        ( select Min(count)
        from
        (
        Select count(c.aid) as count
        from "Cast" as c
        group by c.mid
        order by count desc 
        limit 10
        
        )
        
        )
        order by count desc
       
        
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows



    def q7(self):
        query = '''
        SELECT m.title,female.countF,male.countM
        From 
        (select c.mid,count(a.aid ) as countF
        from Actors as a, "cast" as c
        where c.aid=a.aid AND gender='Female'
        group by mid
        ) as female  join  (
        select c.mid, count(a.aid) as countM
        from Actors as a, "cast" as c
        where c.aid=a.aid AND gender='Male'
        group by mid
        ) as male on male.mid=female.mid, Movies as m
        where  m.mid=male.mid  AND female.countF>male.countM
        order by m.title
      
        
        
        
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q8(self):
        query = '''
        Select a.fname,lname,count(distinct did) as count
        from Actors as a,"Cast" as c, Movie_Director as md
        where a.aid=c.aid AND md.mid=c.mid
        group by a.aid
        having count>=7
        order by count desc
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows


    def q9(self):
        query = '''
        SELECT a.fname,a.lname,count(m.mid) as count
        from Actors as a, "Cast" as c, Movies as m,
        (SELECT c.aid, Min(year) as miniumn
        from "Movies" as m, "Cast" as c 
        where c.mid=m.mid
        group by aid
        ) as x
        WHERE m.year=x.miniumn AND a.aid=c.aid AND m.mid=c.mid AND x.aid=c.aid AND fname like "D%"
        group by a.aid
        order by count desc,fname,lname
        
        
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q10(self):
        query = '''
        Select a.lname,m.title
        from Actors as a, "Cast" as c, Movie_Director as md, Directors as d,movies as m
        where a.aid=c.aid AND md.mid=c.mid AND d.did=md.did AND c.mid=m.mid AND a.lname=d.lname AND a.fname!=d.fname
        order by a.lname,m.title
        
        
            
        '''

        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q11(self):
        query = '''
        select distinct a.fname,a.lname
        from "cast" as c,Actors as a
        where c.mid in
        (
        select distinct c.mid
        from "cast" as c,Actors as a
        where a.aid in 
        (
        Select a.aid
        from "cast" as c,Actors as a
        where c.mid in 
        (
        select distinct c.mid
        from "cast" as c,Actors as a
        where a.aid=c.aid AND a.fname='Kevin' AND a.lname='Bacon')
        
        AND a.aid=c.aid)
        AND a.aid=c.aid)
        AND a.aid=c.aid AND a.aid not in 
        
        (
        select a.aid
        from "cast" as c,Actors as a
        where a.aid in (Select a.aid
        from "cast" as c,Actors as a
        where c.mid in 
        (select distinct c.mid
        from "cast" as c,Actors as a
        where a.aid=c.aid AND a.fname='Kevin' AND a.lname='Bacon')
        AND a.aid=c.aid)
        AND a.aid=c.aid)
        order by lname,fname
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q12(self):
        query = '''
        Select a.fname,a.lname,count(m.mid),avg(m.rank) as averge
        From Actors as a, "Cast" as c, Movies as m
        Where a.aid=c.aid AND m.mid=c.mid
        group by a.aid
        order by averge desc
        limit 20
        
        
        
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

if __name__ == "__main__":
    task = Movie_db("cs1656-public.db")
    rows = task.q0()
    print(rows)
    print()
    rows = task.q1()
    print(rows)
    print()
    rows = task.q2()
    print(rows)
    print()
    rows = task.q3()
    print(rows)
    print()
    rows = task.q4()
    print(rows)
    print()
    rows = task.q5()
    print(rows)
    print()
    rows = task.q6()
    print(rows)
    print()
    rows = task.q7()
    print(rows)
    print()
    rows = task.q8()
    print(rows)
    print()
    rows = task.q9()
    print(rows)
    print()
    rows = task.q10()
    print(rows)
    print()
    rows = task.q11()
    print(rows)
    print()
    rows = task.q12()
    print(rows)
    print()
