# -*- coding: utf-8 -*-

import sys
print('python: {}'.format(sys.version))
import numpy as np
print('numpy: {}'.format(np.__version__))
import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
print('pandas: {}'.format(pd.__version__))

## set plot styles
SMALL_SIZE = 16
MEDIUM_SIZE = 20
BIGGER_SIZE = 28

# latex fonts
matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],'size':SMALL_SIZE})
matplotlib.rc('text', usetex=True)
matplotlib.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
matplotlib.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
matplotlib.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
matplotlib.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
matplotlib.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
matplotlib.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title 
# Include packages `amssymb` and `amsmath` in LaTeX preamble
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amssymb}",r"\usepackage{amsmath}",
											r"\usepackage[utf8x]{inputenc}"]

def piechartgrid(x='None', y='None', data='None', legendmode ='on', legendposition = 'auto', 
				 subfigsize=(2,2), dpi=100, latex=True, **kwargs):

	"""Generates a of pie charts for categorial data. Based on the unique values in dataframe columns ``x`` and ``y`` the grid of subplots is constructed 
	and the associated pie charts are displayed. The corresponding numeric values and labels are drawn.

	The data must be passed in a long-form DataFrame with variables specified by
	passing strings to ``x``, ``y``, and other parameters.

	Extra keyword arguments are passed to the underlying function (matplotlib.pyplot.pie) and (matplotlib.pyplot.legend), so you
	should refer to the documentation for each to see kind-specific options.

	After plotting, the module piechartgrid returns the fig.objects as well as the outer axes. These can
	be used directly to tweak supporting plot details.

	Parameters
	----------
	x, y : names of variables in ``data``
		Input data variables. The latter can be numerica as well as categorial.

	data : DataFrame
		Tidy ("long-form") dataframe where each column is a variable and each
		row is an observation.

	legendmode: 'on|off', optional, default: 'on'
		Controls if legend (default: yes) is displayed.

	legendposition: 'auto|left|right|top|bottom|manual', optional, default: 'auto'
		The location of the legend. Per default, the legend is put at the left side if ``x``-values are negative; otherwise, at the right border of the grid.
		If choosing ``manual`` than the location and bbox_to_anchord passed directly by legendargs are used.

	subfigsize: tuple of floats, optional, default: (1,1)
		width, height in inches. If not provided, defaults to (1,1)
		Fontsizes for tickslabels, axis-labels as well as chart labels are adjusted.

	dpi: integer, optional, default: 100
		resolution of the figure. If not provided, defaults to 100.

	latex: True|False, optional, default: True
		Controls if ticklabels, axes labels, and legend are displayed in LateX encoding.

	**kwargs: keyword arguments passed to the underlying function
		Default setting for pie chart and legend will be updated depending on the keyword arguments

	Returns
	----------

	figure : Figure
		Get the Figure instance.

	axes : Axes
		Get the current :class:`matplotlib.axes.Axes` instance on the
		current figure matching.

	legend : Legend
		Get the current legend instance on the current figure matching.


	Example:
	----------

		# build categorial random input data frame
		x = np.random.rand(100,3)
		x[:,0]=5*x[:,0]
		x[:,1]=5*x[:,1]
		x[:,2]=3*x[:,2]

		x = np.round(x)
		ll = ['a','b','c','d']
		y=np.array([ll[i] for i in x[:,2].astype(int)])
		df = pd.DataFrame(data={'x':x[:,0].T,'y':x[:,1].T,'class':y})
		df = pd.get_dummies(df,prefix='',prefix_sep='')

		# keyword arguments for matplotlib.pyplot.pie and matplotlib.pyplot.legend
		piekwargs = {'radius' :1, 'autopct' : "%.1f%%", 'pctdistance' : 0.6, 'shadow':True, 'explode':[0,0.2,0,0],
				'wedgeprops' : {'linewidth': 0},
				'textprops' : {'color':"white"}
			}
		legendkwargs = {'fontsize':10,'frameon':False, 'ncol':1,'labelspacing':0.2}

		fig, ax, leg = piechartgrid(x='x',y='y', data=df, legendposition='auto', subfigsize=(1,1), dpi=300,
						**{'pieargs':piekwargs,'legendargs':legendkwargs})

	Notes:
	-----------

	Tested under Python (3.6.5), numpy (1.14.3), matplotlib (2.2.2), and pandas (0.23.0).

	"""

	if not isinstance(x,str) or  x=='None':
		raise Exception('x is either not defined or not a string')
	elif not isinstance(y,str) or  y=='None':
		raise Exception('y is either not defined or not a string')
	
	# check input dateframe
	if data is not None:
		try:
			if data.empty:
				raise ValueError('dataframe is empty')
		except AttributeError as err:
			raise AttributeError('data is not a pandas.DataFrame')  
	else:
		raise AttributeError('input data is not defined')
		
	# get type for x column
	if 'float' in str(data[x].dtype):
		xtickformat = '.2f'
		xrot = 0
		xha = 'center'
		isnum = True
	elif 'int' in str(data[x].dtype):
		xtickformat = 'd'
		xrot = 0
		xha = 'center'
		isnum = True
	elif 'object' in str(data[x].dtype):
		xtickformat = ''
		xrot = 45
		xha = 'right'
		isnum = False
	else:
		raise AttributeError('x data is neither int, float, or object')
	 
	# get type for y column
	if 'float' in str(data[y].dtype):
		ytickformat = '.2f'
		yrot = 0
		yha = 'center'
	elif 'int' in str(data[y].dtype):
		ytickformat = 'd'
		yrot = 0
		yha = 'center'
	elif 'object' in str(data[y].dtype):
		ytickformat = ''
		yrot = 0
		yha = 'right'
	else:
		raise AttributeError('y data is neither int, float, or object')
	
	
	# subfigure size
	(subsizex,subsizey) = subfigsize
	scale = min(subsizex,subsizey)
	
	SMALLF = float(scale*8)
	MEDF = float(scale*16)
	LARGEF = float(scale*20)
	
	# x and y values
	xval = np.unique(data[x].values); ncol = len(xval)
	yval = np.unique(data[y].values)[::-1]; nrow = len(yval)
	XX, YY = np.meshgrid(xval,yval)
		
	## create figure
	fig = plt.figure(figsize=(subsizex*ncol,subsizey*nrow), dpi=dpi)
	outer = gridspec.GridSpec(1, 1, wspace=0.1, hspace=0.1,figure=fig)
	axout = fig.add_subplot(outer[0])
	
	inner = gridspec.GridSpecFromSubplotSpec(nrow, ncol,
						subplot_spec=outer[0], wspace=0, hspace=0.)
			
	# legendmode
	if legendmode=='on':
		legon = True
	elif legendmode=='off':
		legon = False
	else:
		raise AttributeError('accepted legend attributes are: on{default}|off')

	# auto-dection of optimal legend position
	if legendposition == 'auto':
		if isnum and xval[0]<0:
			legendposition = 'left'
		else:
			legendposition = 'right'
					
	# switch on or off latex typsetting
	matplotlib.rc('text', usetex=latex)
	
	# default setting for pie chart
	defpiekwargs = {'radius':0.9, 'autopct':"%.1f%%", 'pctdistance':0.5,
				   'wedgeprops' : {'linewidth': 0},
				   'textprops' : {'fontsize':SMALLF, 'fontweight':'heavy','color':"white"}
				  }
	# default setting for legend
	deflegendkwargs = {'frameon':False, 'ncol':1, 'fontsize' : MEDF, 'labelspacing':1}
	
	# update pie and legend settings by kwargs
	pieargs = defpiekwargs
	legendargs = deflegendkwargs
	for key, value in kwargs.items():
		if key.find("pie") != -1: 
			for subkey, subval in value.items():
				try:
					pieargs[subkey].update(subval)
				except:
					pieargs[subkey] = subval
		elif key.find("legend") != -1: 
			for subkey, subval in value.items():
				try:
					legendargs[subkey].update(subval)
				except:
					legendargs[subkey] = subval
		else:
			raise TypeError('an unexpected keyword argument {}'.format(key))

	# latex formating of legend title
	try:
		legendargs['title'] = latextext(legendargs['title']) 
	except:
		pass
	
	if (legendposition is not 'manual') and ('loc' in legendargs or 'bbox_to_anchor' in legendargs):
		print('Warning: user defined values for loc and bbox_to_anchor will be deleted.\r\n Use manual instead.')
			
	# manual setting of legend and label positions
	if legendposition == 'left':
		axout.spines['top'].set_visible(False)
		axout.spines['left'].set_visible(False)
		axout.yaxis.set_label_position("right")
		axout.yaxis.tick_right()
		legendargs.update({'loc':"center right",'bbox_to_anchor':(-.02, 0.5)})
	elif legendposition == 'right':
		axout.spines['top'].set_visible(False)
		axout.spines['right'].set_visible(False)
		legendargs.update({'loc':"center left",'bbox_to_anchor':(1.02, 0.5)})
	elif legendposition == 'top' and isnum and xval[0]<0:
		axout.spines['top'].set_visible(False)
		axout.spines['left'].set_visible(False)
		axout.yaxis.set_label_position("right")
		axout.yaxis.tick_right()
		legendargs.update({'loc':"lower center",'bbox_to_anchor':(0.5, 1.02)})
	elif legendposition == 'top':
		axout.spines['top'].set_visible(False)
		axout.spines['right'].set_visible(False)
		legendargs.update({'loc':"lower center",'bbox_to_anchor':(0.5, 1.02)})
	elif legendposition == 'bottom' and isnum and xval[0]<0:
		axout.spines['bottom'].set_visible(False)
		axout.spines['left'].set_visible(False)
		axout.xaxis.set_label_position("top")
		axout.xaxis.tick_top()
		axout.yaxis.set_label_position("right")
		axout.yaxis.tick_right()
		legendargs.update({'loc':"upper center",'bbox_to_anchor':(0.5, -0.02)})
	elif legendposition == 'bottom':
		axout.spines['bottom'].set_visible(False)
		axout.spines['right'].set_visible(False)
		axout.xaxis.set_label_position("top")
		axout.xaxis.tick_top()
		legendargs.update({'loc':"upper center",'bbox_to_anchor':(0.5, -0.02)})
	elif legendposition == 'manual':
		pass
	else:
		raise AttributeError('accepted legendpositions are: auto{default}|left|right|bottom|top|manual')

	# reduced data frame
	df = data.drop(columns=[x,y])
	classes = [latextext(i) for i in df.columns]
		
	for idx, ([xx], [yy]) in enumerate(zip(XX.reshape((-1,1)),YY.reshape((-1,1)))):
		ax = fig.add_subplot(inner[idx])
		ax.axis('equal')
		
		tmp = df.loc[np.logical_and(data[x]==xx , data[y]==yy)]
		if not tmp.empty:
			dist=[i for i in tmp.mean()]
			wedges, texts, autotexts = ax.pie(dist, **pieargs)
			 
			for txt in autotexts:
				# hide 0.0% autotexts
				if txt.get_text()[0]=='0':
					txt.set_visible(False)
				# change label position to center if only one wedge exists
				elif len(txt.get_text()) or (txt.get_text().find("none") != -1):
					txt.set_visible(False)
				elif txt.get_text()[:3]=='100':
					txt.set_position([0,0])
				# latex formating
				txt.set_text(r'${0}$'.format(txt.get_text().replace('%','\%')))
		else:
			ax.set_visible(False)
		
	# make frame lines thicker
	[sp.set_linewidth(2*scale) for sp in axout.spines.values()]
			
	axout.xaxis.set_tick_params(size=5*scale,width=2*scale)
	axout.xaxis.set_ticks(np.arange(1/(2*ncol),1,1/ncol))
	#axout.xaxis.set_ticklabels([r'${:.2f}$'.format(j) for j in xval],fontsize=MEDF)
	axout.xaxis.set_ticklabels([r'${0:{1}}$'.format(j,xtickformat) for j in xval],
								rotation = xrot, ha = xha, fontsize=MEDF)
	#xlbl = axout.set_xlabel(r'${}$'.format(x.replace(' ','\,')),fontsize=LARGEF)
	xlbl = axout.set_xlabel(latextext(x),fontsize=LARGEF) 
	
		
	axout.yaxis.set_tick_params(size=5*scale,width=2*scale)
	axout.yaxis.set_ticks(np.arange(1/(2*nrow),1,1/nrow))
	axout.yaxis.set_ticklabels([r'${0:{1}}$'.format(j,ytickformat) for j in yval[::-1]],
								rotation = yrot, fontsize=MEDF)
	#ylbl = axout.set_ylabel(r'${}$'.format(y.replace(' ','\,')),fontsize=LARGEF) 
	ylbl = axout.set_ylabel(latextext(y),fontsize=LARGEF) 
	
	# display legend
	if legon:
		leg = axout.legend(wedges, classes,**legendargs) 
		leg.get_title().set_fontsize(str(LARGEF)) # matplotlib vers < 3.0
	
	return fig, axout, leg

def latextext(instring):
	return r'$\mathrm{'+'{}'.format(instring.replace(' ','\,'))+'}$'