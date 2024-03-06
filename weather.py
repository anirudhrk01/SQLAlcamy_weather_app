from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os

load_dotenv()

app=Flask(__name__)

@app.route('/',methods=['POST','GET'])

def weather_info():
    api_key='436ac2860e3609b1a8191b05153947ab'

    if request.method=='POST':
            lat=request.form.get('latitude')
            lon=request.form.get("longitude")
            url=f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
            print(url)
            response=requests.get(url)
            weather_data=response.json()
            try:
              temp_celsius=round(weather_data['main']['temp']-273.15,1)
              weather=weather_data['weather'][0]['main']
              city_name=weather_data['name']
              icon=weather_data['weather'][0]['icon']

              return render_template("index.html",temp_celsius=temp_celsius,weather=weather,city_name=city_name,icon=icon)
            
            except KeyError as e:
              print(f"KeyError :{e}") 
              return render_template("index.html",error_message="Failed to retrieve weather information.")  
                 
    return render_template("index.html")


app.run()