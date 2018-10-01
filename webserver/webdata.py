from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import datetime
from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)
import sqlite3
conn=sqlite3.connect('../assignment.db')
curs=conn.cursor()

# reference: https://www.hackster.io/mjrobot/from-data-to-graph-a-web-journey-with-flask-and-sqlite-4dba35
def getLastData():
	for row in curs.execute("SELECT * FROM sensehat_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
		hum = row[2]
	return time, temp, hum

def getHistData ():
	curs.execute("SELECT * FROM sensehat_data ORDER BY timestamp DESC LIMIT 24")
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
	for row in reversed(data):
		dates.append(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"))
		temps.append(row[1])
		hums.append(row[2])
	return dates, temps, hums

@app.route("/")
def index():
	time, temp, hum = getLastData()
	templateData = {
	  	'time'	: time,
		'temp'	: temp,
      	'hum'	: hum,
	}
	return render_template('index.html', **templateData)

@app.route('/plot/temp')
def plot_temp():
	times, temps, hums = getHistData()
	ys = temps
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature")
	axis.set_xlabel("Date")
	axis.grid(True)
	xs = times
	axis.plot(xs, ys)
	fig.autofmt_xdate()
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/hum')
def plot_hum():
	times, temps, hums = getHistData()
	ys = hums
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Humidity")
	axis.set_xlabel("Date")
	axis.grid(True)
	xs = times
	axis.plot(xs, ys)
	fig.autofmt_xdate()
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=False)