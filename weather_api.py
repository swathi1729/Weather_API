#Imported packages
import requests, json, csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Necessary varibles to make an API call

#Kindly fill necessary variable details
city = "Bengaluru"
api_key = "9becbb9b127fd57b265c8de972b3272f"
api_endpoint = "https://api.openweathermap.org/" 
url= api_endpoint+"/data/2.5/forecast?q="+city+"&appid="+api_key
json_file_path="d:/weather_data_file.json"
csv_file_path="d:/weather_data_file.csv"
api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"


def weather_report(url):
    '''
    weather_report() function takes one argument to make an api call through the url to get the data to returns json object
    
    '''
    try :
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
        else:
            raise Exception("Failed to connect to API")
        return weather_data
    except Exception as e:
        print(f"Exception raised from weather_report() function : {e}")

def json_file(json_file_path):
    '''
    json_file() function reads the json object and converts into json file return json filepath
    
    '''
    try :
        with open(json_file_path, "w") as jf:
            json.dump(weather_report(url),jf,indent=4)
        return json_file_path
    except Exception as e:
        print(f"Exception raised from json_file() function : {e}")

def read_json():
    '''
    read_json() functuion used to read the json file and returns weather_info and date list values
    '''
    try:
        js_file_path=json_file(json_file_path)
        with open(js_file_path,'r') as jf:
            json_data = json.load(jf)
        data_file = open(csv_file_path, 'w', newline='')
        csv_writer = csv.writer(data_file)
        ls=json_data["list"]
        weather=[]
        date_value=[]
        count = 0
        for num in range(len(ls)):
            weather.append(ls[num]["main"])
            weather.append(ls[num]["wind"])
            date_value.append(ls[num]["dt_txt"])
        return weather,date_value
    except Exception as e:
        print(f"Exception raised from read_json() function : {e}")
    
def convert_to_csv(csv_file_path):
    '''
    convert_to_csv(csv_file_path) file takes one argument as csv file path to write return csv data file path
    '''
    try:
        weather,date_value=read_json()
        temp= pd.DataFrame(weather)['temp'].tolist()
        pressure= pd.DataFrame(weather)['pressure'].tolist()
        humidity= pd.DataFrame(weather)['humidity'].tolist()
        speed=pd.DataFrame(weather)['speed'].tolist()
        weather_dict = {'temperature': temp, 'pressure': pressure, 'humidity': humidity,'speed':speed,'date':date_value} 
        weather_list=[temp,pressure,humidity,speed,date_value]
        fields = ['temperature', 'pressure', 'humidity','speed','date']
        with open(csv_file_path, "w", newline='') as outfile:
            writerfile = csv.writer(outfile)
            writerfile.writerow(weather_dict.keys())
            writerfile.writerows(zip(*weather_dict.values()))
        return csv_file_path
    except Exception as e:
        print(f"Exception raised from convert_to_csv() function : {e}")
        
def read_csv():
    '''
    read_csv() function reads the csv using pandas and returns dataframe
    '''
    try:
        csv_path=convert_to_csv(csv_file_path)
        data = pd.read_csv(csv_path)
        df = pd.DataFrame(data)
        #df.fillna(0)
        df['temperature'] = df['temperature'].fillna(0)
        df['pressure'] = df['pressure'].fillna(0)
        df['humidity'] = df['humidity'].fillna(0)
        df['speed'] = df['speed'].fillna(0)
        df['date'] = df['date'].fillna(0)
        df['date'] = pd.to_datetime(df['date']).dt.date
        df.to_csv(csv_path,index=False)
        return df
    except Exception as e:
        print(f"Exception raised from read_csv() function : {e}")


def plot_temperture_graph():
    '''
    plot_temperture_graph() function used to plot the temperature bar graph
    '''
    try:
        df=read_csv()
        x = np.array(df["date"])
        y = np.array(df["temperature"])
        plt.title("Temperature over 5 days")
        plt.xlabel("Date")
        plt.ylabel("Temperature")
        plt.bar(x, y, width =0.2)
        plt.show()
    except Exception as e:
        print(f"Exception raised from plot_temperture_graph() function : {e}")
def plot_pressure_graph():
    '''
    plot_pressure_graph() function used to plot the pressure bar graph
    '''
    try :
        df=read_csv()
        x = np.array(df["date"])
        y = np.array(df["pressure"])
        plt.title("Pressure over 5 days")
        plt.xlabel("Date")
        plt.ylabel("Pressure")
        plt.bar(x, y, width =0.2)
        plt.show()
    except Exception as e:
        print(f"Exception raised from plot_pressure_graph() function : {e}")
def plot_humidity_graph():
    '''
    plot_humidity_graph() function used to plot the humidity bar graph
    '''
    try:
        df=read_csv()
        x = np.array(df["date"])
        y = np.array(df["humidity"])
        plt.title("Humidity over 5 days")
        plt.xlabel("Date")
        plt.ylabel("Humidity")
        plt.bar(x, y, width =0.2)
        plt.show()
    except Exception as e:
        print(f"Exception raised from plot_humidity_graph() function : {e}")
def plot_wind_speed_graph():
    '''
    plot_wind_speed_graph() function used to plot the wind speed bar graph
    '''
    try:
        df=read_csv()
        x = np.array(df["date"])
        y = np.array(df["speed"])
        plt.title("Wind Speed over 5 days")
        plt.xlabel("Date")
        plt.ylabel("Wind Speed")
        plt.bar(x, y, width =0.2)
        plt.show()
    except Exception as e:
        print(f"Exception raised from plot_wind_speed_graph() function : {e}")

def weather_info(api_url):
    '''
    weather_info() gives weather info details
    
    '''
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            weather_data= response.json()
            temp=weather_data["main"]["temp"]
            humidity=weather_data["main"]["humidity"]
            sunrise=weather_data["sys"]["sunrise"]
            sunset=weather_data["sys"]["sunset"]
            name=weather_data["name"]
            print('-'*10+"Weather_info"+'-'*10)
            print(f"{name}\nTemperature : {temp}\nHumidity : {humidity}\nSunrise : {sunrise}\nSunset : {sunset}")
        else:
            raise Exception("Failed to connect to api")
    except Exception as e:
        print(f"Exception raised from weather_info() function : {e}")

if __name__ == "__main__":
    weather_info(api_url)
    plot_temperture_graph()
    plot_pressure_graph()
    plot_humidity_graph()
    plot_wind_speed_graph()
    
    