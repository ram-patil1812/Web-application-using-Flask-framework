# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 14:33:00 2021

@author: Ramchandra patil
"""

from flask import Flask,render_template,request,redirect #import flask module and import Flask class from flask module 
import pymysql # pymysql is used to connect py file to dbms.
app=Flask(__name__)


@app.route("/")
def index():
    # fetching data from task in database into data in "d" variable and show in dashboard
    try:
        db=pymysql.connect(host="localhost",user="root",password="",db="todo")
        cu=db.cursor()
        sql="select * from task"
        cu.execute(sql)
        data=cu.fetchall()
        
        #return"All records fetched"
        return render_template("dashboard.html",d=data)
    
    except Exception:
        return "Error in connection"
        

@app.route("/form")
def form():
    
    return render_template("form.html")

@app.route("/insert",methods=["POST","GET"]) # it is syntax when we submit the form
def insert():                                # methods=["POST","GET"]

    t=request.form["title"]  #request is a function to extract the data from keys.
    det=request.form["detail"] #form is dictionary storage we always request from form for values.
    dt=request.form['date'] # in other word form is storage of key-value pair. 
    
    #return t+det+dt

    try:
        db=pymysql.connect(host="localhost",user="root",password="",db="todo")
        cu=db.cursor()
        sql="insert into task(title,detail,date)values('{}','{}','{}')".format(t,det,dt)
        cu.execute(sql)
        db.commit()
        return redirect("/") #redirect is used to go return to dashboard
    
    except Exception:
        return "Error in connection"
    
@app.route("/delete/<rid>")
def delete(rid):
    # rid is recorted id which is selected by user
    #return "ID is : " + id
    try:
        db=pymysql.connect(host="localhost",user="root",password="",db="todo")
        cu=db.cursor()
        sql="delete from task where id = '{}'".format(rid) # here id is column in data table and task is table name.
        cu.execute(sql)
        db.commit() # commit is function used to save the data when existing data is change aur edit or delete and insert.
        return redirect('/')
    
    except Exception:
        return "Connection failed"

@app.route("/edit/<rid>")
def edit(rid):
    
    #return "Edit ID is : " + rid
    #return render_template("edit_form.html")
    
    try:
        db=pymysql.connect(host="localhost",user="root",password="",db="todo")
        cu=db.cursor()
        sql="select * from task where id='{}'".format(rid)
        cu.execute(sql)
        data=cu.fetchone()
        return render_template('edit_form.html',d=data)
    
    except Exception:
        return "Connection failed"
    
@app.route("/update",methods=["POST","GET"])
def update():
    
    t = request.form["title"]
    det = request.form["detail"]
    dt = request.form["date"]
    rid = request.form["rid"]
    
    #return t+det+dt+rid
    
    try:
        db=pymysql.connect(host="localhost",user="root",password="",db="todo")
        cu=db.cursor()
        sql="update task SET title='{}',detail='{}',date='{}' where id='{}'".format(t,det,dt,rid)
        cu.execute(sql)
        db.commit()
        return "Record updated succesfully"
    
    except Exception:
        
        return "Failed to update record"
        
app.run(debug=True)  # this line always present at last of code which is run your whole program
                     # program must end with this line to run the app.
                     # to ON debug mode run(debug=true)
                     # by default debug mode is off

