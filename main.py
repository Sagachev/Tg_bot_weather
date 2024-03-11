import telebot
import requests
import json
import settings

bot = telebot.TeleBot(settings.Token_bot)
API = '2d4661fe35068871f574d840d497903e'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название города в котором хочешь узнать погоду')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru')

    if res.status_code != 200:
        bot.reply_to(message, f'Кажется такого города не существует \U0001F914')
    else:
        data = json.loads(res.text)
        temp = int(data["main"]["temp"])
        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Скорее всего это конец света \U0001F633'
        humidity = data['main']['humidity']
        pressure = int(data['main']['pressure'])
        pressure_mm = int(pressure / 1.33)
        wind_speed = int(data['wind']['speed'])
        bot.reply_to(message,
                     f'Сейчас в городе {data["name"]} \n{wd}'
                     f'\nТемпература: {temp}Cº  \nВлажность:  {humidity} %'
                     f'\nДавление: {pressure_mm} мм рт.ст. \nСкорость ветра: {wind_speed} м/с')


bot.polling(none_stop=True)
