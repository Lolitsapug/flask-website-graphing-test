from flask import Flask, render_template, request, flash, redirect
from matplotlib import pyplot as plt
from io import BytesIO
import sqlite3,base64
import GPy
import numpy as np
import matplotlib-inline


%matplotlib inline
%config InlineBackend.figure_format = 'svg'
import matplotlib;matplotlib.rcParams['figure.figsize'] = (8,5)

GPy.plotting.change_plotting_library("matplotlib")

# sample inputs and outputs
X = np.random.uniform(-3.,3.,(20,1))
Y = np.sin(X) + np.random.randn(20,1)*0.05
# define kernel
kernel = GPy.kern.RBF(input_dim=1, variance=1., lengthscale=1.)
GPy.kern.BasisFuncKernel
# create simple GP model
m = GPy.models.GPRegression(X,Y,kernel)
# optimize and plot
m.optimize()
fig = m.plot()
GPy.plotting.show(fig, filename='basic_gp_regression_notebook')
fig.savefig("model.pdf")
tmpfile = BytesIO()
fig.savefig(tmpfile, format='png')
tmpfile.seek(0)
encoded = base64.b64encode(tmpfile.getvalue()).decode('utf8')

highest = 0
for i in range(len(Y)):
	if Y[i][0] > highest :
		highest = Y[i][0]
		print(highest)


amplitude = ""
wavePeriod = ""
waterDepth = ""
cylinderDiameter = ""


app = Flask(__name__) 
app.config['SECRET_KEY'] = '7cb54c3f6dd605fcd57bd1e07641f51409445880eb962255'


@app.route('/')
def index():
	return render_template('index.html') #renders index page


@app.route('/input/', methods=('GET', 'POST'))
def input():
	global amplitude, wavePeriod, waterDepth, cylinderDiameter
	if request.method == 'POST': #gets data from input page
		amplitude = request.form['Data1']
		wavePeriod = request.form['Data2']
		waterDepth = request.form['Data3']
		cylinderDiameter = request.form['Data4']
		if not amplitude or not wavePeriod or not waterDepth or not cylinderDiameter: 
			flash('Fill all the data!') #checks all inputs filled and if not tells user to fill all
		else:
			return redirect("/graph/")
			#return graph(amplitude,wavePeriod,waterDepth,cylinderDiameter)
			#runs graph function
			
	return render_template('input.html') #renders input page


@app.route('/graph/')
def graph():
	return render_template('graph.html', d1=amplitude, d2=wavePeriod, d3=waterDepth, d4=cylinderDiameter, graphName = "exampleGraph.jpg", base64=encoded, yTop=highest)
	#renders graph.html passing the variables



app.run(host='0.0.0.0', port=8080)
