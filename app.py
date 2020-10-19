import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
	new_city = 'New Delhi'
	if request.method == 'POST':
		new_city = request.form.get('city_name')
	if new_city == "":
		return redirect("/")
	url='http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=059d6ee581988e6cf0df98e9abaf5359'
	report = requests.get(url.format(new_city)).json()
	weather = {
		'city': new_city,
		'country': report['sys']['country'],
		'temperature': report['main']['temp'],
		'description': report['weather'][0]['description'],
		'humidity': report['main']['humidity'],
		'icon' : report['weather'][0]['icon']
	}
	return render_template('index.html',  weather=weather)

if __name__ == '__main__':
	app.run(debug=True)