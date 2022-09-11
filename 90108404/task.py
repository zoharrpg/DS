import sqlite3 as lite
import csv
import re
import pandas as pd


class Task(object):
    def __init__(self, db_name):
        self.con = lite.connect(db_name)
        self.cur = self.con.cursor()

    #q0 is an example 
    def q0(self):
        query = '''
            SELECT COUNT(*) FROM students
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    
    def q1(self):
        query = '''
        select firstName,lastName From students where yearStarted=2019

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
        

    def q2(self):
        query = '''
        select firstName, lastName From students, Majors where students.sid=Majors.sid AND (Majors.major='CS' or Majors.major='COE' )

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q3(self):
        query = '''
        select COUNT(firstname) FROM students,Majors where students.sid=Majors.sid AND(Majors.major='ASTRO')

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows


    def q4(self):
        query = '''
        select firstName, lastName,yearStarted,Sum(credits) from students, grades 
        where students.sid = Grades.sid AND Grade>0
        Group by Grades.sid
        
        
        
        


        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q5(self):
        query = '''
        select Professor,COUNT(cid) from Courses
        Group by Professor

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q6(self):
        query = '''
        
        select cid,grade, count(*) from GRADES
        Group by cid,grade
       
        
        

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q7(self):
        query = '''
         select cid,grade, count(*) from GRADES where grade=4
        Group by cid,grade
       

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

if __name__ == "__main__":
    task = Task("students.db")
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
