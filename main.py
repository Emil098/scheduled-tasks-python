# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


import os
import requests
import smtplib

API_KEY = os.environ.get("WEATHER_API_KEY")
EMAIL_KEY = os.environ.get("EMAIL_KEY")
print(f"API KEY - {API_KEY}")
MY_LAT = 51.246910
MY_LONG = 22.573620
API_URL = "https://api.openweathermap.org/data/2.5/forecast"

params = {
    "lon": MY_LONG,
    "lat": MY_LAT,
    "cnt": 4,
    "appid": API_KEY
}


response = requests.get(url=API_URL, params=params)
print(response)
response.raise_for_status()

data = response.json()
print(data)

def create_mail_content(subject, mail_body):
    return f"Subject:{subject}\n\n{mail_body}"

def send_mail(dst_email, email_subject, message):
    my_email = "emil.testy22@gmail.com"
    pwd = EMAIL_KEY

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=pwd)
        print("logged in")
        connection.sendmail(from_addr=my_email,
                            to_addrs=dst_email,
                            msg=create_mail_content(email_subject, message))
condition_desc_list = []
temp_list = []

for forecast in data["list"]:
    for condition in forecast["weather"]:
        if condition["description"] not in condition_desc_list:
            condition_desc_list.append(condition["description"])
    temp_list.append(float(forecast["main"]["temp"]) - 273.15)

# sprawdzanie tylko pierwszego słownika prognozy
# condition_codes = [int(condition["weather"][0]["id"]) for condition in data["list"]]
# condition_codes = [condition["weather"][0]["id"] for condition in data["list"]] °

temp_avg = sum(temp_list) / len(temp_list)
body = f"Average temperature - {round(temp_avg,1)} degC\n"
body += "Weather Conditions:\n"
for desc in condition_desc_list:
    body += f"{desc}\n"

send_mail("maciej.tkacz19@gmail.com","Pogoda na dzisiaj", body)

