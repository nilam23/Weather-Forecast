import requests
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from os import environ

load_dotenv('.env')

# creating an instance of the flask app
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
	# the default city
	new_city = 'Guwahati'

	# when the user requests a forecast for a particular city
	if request.method == 'POST':
		new_city = request.form.get('city_name')

	# when the user requests for  forecast without any input
	if new_city == "":
		return redirect("/")

	# getting the API KEY
	API_KEY = environ.get('APIKEY')

	# calling the weather API and fetching the corresponding forecast
	url='http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'

	report = requests.get(url.format(new_city, API_KEY)).json()

	# if input city is invalid or no report can be found for the city
	if report['cod'] == '404':
		return render_template('index.html', weather={})

	# extracting the forecast
	weather = {
		'city': new_city,
		'country': report['sys']['country'],
		'temperature': report['main']['temp'],
		'description': report['weather'][0]['description'],
		'humidity': report['main']['humidity'],
		'icon' : report['weather'][0]['icon']
	}

	# rendering the home page with the weather forecast
	return render_template('index.html',  weather=weather)

if __name__ == '__main__':
	app.run(debug=True)