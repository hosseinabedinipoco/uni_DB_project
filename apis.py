import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
#...import fastapi packages.......
from fastapi import FastAPI,Query,Path, Body, Header 
from pydantic import BaseModel, Field
from typing import Optional ,Union,Tuple ,Annotated
#...import fastapi packages.......
from models import Advertise





#import pass from env variable
load_dotenv()
mysql_password = os.getenv('mysql_password')

app = FastAPI() 

# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", #enter your mysql username
    password = mysql_password ,
    database = "Project"
)

cursor = mydb.cursor() # create an instance of cursor class to execute mysql commands





#amiralis apis.....................................................................

@app.post("/{publisher_id}/advertise")
async def publish_advertise(a1: Advertise,publisher_id: int):
    today = datetime.now()
    two_weeks_later = today + timedelta(weeks=2)
    expiration_date = two_weeks_later.strftime('%Y-%m-%d %H:%M:%S')


    cursor.execute(f"""
    INSERT INTO advertise (expiration_date, published_at, price, title, 
    description, status, phone_number, city, publisher_id,type , deleted)
    VALUES ('{expiration_date}', '{today}', {a1.price}, '{a1.title}', '{a1.description}', 'pending', '{a1.phone_number}',
    '{a1.city}',{publisher_id},(SELECT cat_id FROM category WHERE name = '{a1.type_name}'), FALSE);""")

    mydb.commit()

    return f'advertise with {a1.title} is registered'


@app.patch("/advertise/{advertise_id}",response_model=dict)
async def visit_advertise(advertise_id:int):

    cursor.execute(f"""
    select published_at,price,title,phone_number,city,
    (select c.name from category as c where c.cat_id = a.type)
    from advertise as a 
    where a.ad_id = {advertise_id} and a.status = 'accepted' """)

    result = cursor.fetchone()

    cursor.execute(f"""
    update advertise 
    set view = view + 1
    where advertise.ad_id = {advertise_id}
    """)

    mydb.commit()


    response = {
        "title: ":result[2],
        "published_at: ":str(result[0]),
        "price: ":result[1],
        "category: ":result[5],
        "comminucate_way: ":result[3],
        "city: ":result[4],
    }

    return response



#amiralis apis.....................................................................

# cursor.execute("drop database project") #example of how run sql command on file 

