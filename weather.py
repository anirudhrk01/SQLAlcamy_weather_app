from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os

load_dotenv()

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Weather(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    latitude=db.Column(db.Float,nullable=False)
    longitude=db.Column(db.Float,nullable=False)
    temperature=db.Column(db.Float)
    weather = db.Column(db.String(50))
    city_name = db.Column(db.String(50))
    icon = db.Column(db.String(10))
    timestamp=db.Column(db.DateTime, default=datetime.utcnow)


api_key=os.getenv('api_key')
@app.route('/',methods=['POST','GET'])

def weather_info():
    

    if request.method=='POST':
            lat=request.form.get('latitude')
            lon=request.form.get("longitude")
            weather_entry = Weather.query.filter_by(latitude=lat, longitude=lon) \
                                     .filter(Weather.timestamp >= datetime.utcnow() - timedelta(minutes=10)) \
                                     .first()
            
            if weather_entry:
                return render_template("index.html", temp_celsius=weather_entry.temperature,
                               weather=weather_entry.weather, city_name=weather_entry.city_name,
                               icon=weather_entry.icon)




            url=f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
            print(url)
            response=requests.get(url)
            if response.status_code==200:
            
                
                try:
                    weather_data=response.json()
                    temp_celsius=round(weather_data['main']['temp']-273.15,1)
                    weather=weather_data['weather'][0]['main']
                    city_name=weather_data['name']
                    icon=weather_data['weather'][0]['icon']

                    new_weather_entry = Weather(latitude=lat, longitude=lon, temperature=temp_celsius,
                                         weather=weather, city_name=city_name, icon=icon)
                    db.session.add(new_weather_entry)
                    db.session.commit()

                    return render_template("index.html",temp_celsius=temp_celsius,weather=weather,city_name=city_name,icon=icon)
            
                except KeyError as e:
                    print(f"KeyError :{e}") 
                    return render_template("index.html",error_message="Failed to retrieve weather information.")  
            else:
                return render_template("index.html", error_message=f"Unable to fetch weather data. API returned {response.status_code}  ")     
    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)