#coding=utf-8
#import shelve
import MySQLdb
from datetime import datetime
import sys
from flask import Flask,g,request,render_template,redirect,escape,Markup
from re import template
app=Flask(__name__)
app.debug = True
#from config import MYSQL_HOST, MYSQL_PORT,MYSQL_USER, MYSQL_PASS,MYSQL_DB

from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)


        
@app.before_request
def before_request():
    g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS,
                           MYSQL_DB, port=int(MYSQL_PORT))

def save_data(name,words,create_at):
    #sava the comment data
    visit_info=[name,words,create_at]
    #use mysql database
    #get a cursor
    curs=g.db.cursor()
    curs.execute("insert into visit values(%s,%s,%s)",visit_info)
    curs.execute('alter table visit order by visit_at desc')
    g.db.commit()
    curs.close()
    g.db.close()
    
def  load_data():
        #return the comments savaed before
        #open the shelve module database file
        #use mysql to return
        curs=g.db.cursor()
        curs.execute("select * from visit")
        visit_info=curs.fetchall()
        curs.close()
        g.db.close()
        return visit_info

@app.route('/')
def index():
    #Top Page
    #Use template to show the Page
    visit_list=load_data()
    return render_template('index.html',visit_list=visit_list)
@app.route('/post',methods=['POST'])
def post():
    #Comment's target url
    #get the comment data
    name=request.form.get('name')
    words=request.form.get('comments')
    create_at=datetime.now()
    #save the data
    save_data(name,words,create_at)
    return redirect('/')

@app.template_filter('nl2br')
def nl2br_filters(s):
    #tranform the new line in comment to </br> tag
    return escape(s).replace('\n', Markup('</br>'))

@app.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    #make the datetime to be shown friendly
    return dt.strftime('%Y-%m-%d %H:%M:%S')