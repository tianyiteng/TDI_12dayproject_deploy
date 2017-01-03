# Import Dependencies
import config as con
import datetime
import quandl
import pandas as pd
import os
from bokeh.charts import output_file, TimeSeries
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)

app.config.from_object(__name__)

# Load default config 
app.config.update( dict(
	SECRET_KEY = 'development key',
	))

# Initialize Dates method
quandl.ApiConfig.api_key = con.QUANDL_API_KEY
current_month = datetime.date.today().month
prior_month = current_month - 1
year = datetime.date.today().year


# ---------------------------------------------------------------------------
@app.route('/')
def main():
  return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
	# Pull POST data for 'ticker' into a local variable
	if request.method == 'POST':
		ticker = request.form['ticker']

		ticker_data = quandl.get('WIKI/' + ticker, collapse='daily')

		# Create title for Bokeh plot 
		title = ('Daily Closing Stock Price for ' + ticker + ', ' + str(prior_month) + '/' + str(year) + ' - ' + str(current_month) + '/' + str(year))

		# Create bokeh plotting variable
		ts_plot = TimeSeries(ticker_data.Close[-30:], title = title, xlabel = 'Date', ylabel = 'Price ($ USD)')

		script, div = components(ts_plot)

		return render_template('plot.html', script=script, div=div)
	else:
		return render_template('index.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)