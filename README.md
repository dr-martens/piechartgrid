# What is piechartgrid?

Piechartgrid is a python module to display the dependence of classes on specific features. The latter can be either numeric or categorial. Piechartgrid bases on the pie module from matplotlib. Any commands controlling for the appearence of the pies as well as the legend design can be passed directly. Additionally, per default all texts and values are shown in Latex style.

# How to load piechartgrid

After downloading the git repository, you can add the module to the python path by using

```
import sys
sys.path.insert(0, '\path\to\my\libs\')
```

Then one can import piechartgrid

```
from piechartgrid import *
```

The module loads any neccessary package like numpy, matplotlib, and pandas.

For further informations about piechartgrid, please type

```
help(piechartgrid)
```

# Examples
### Example 1

```
x = np.random.rand(100,3)
x[:,0]=5*x[:,0]
x[:,1]=5*x[:,1]
x[:,2]=3*x[:,2]

x = np.round(x)
ll = list('abcdefghijk')
y=np.array([ll[i] for i in x[:,1].astype(int)])
z=np.array([ll[i] for i in x[:,2].astype(int)])
df = pd.DataFrame(data={'x':x[:,0].T,'y':y,'class':z})
df = pd.get_dummies(df1,columns=['class'],prefix='',prefix_sep='')

piekwargs = {'radius' :1, 'autopct' : "%.1f%%", 'pctdistance' : 0.6, 'shadow':False,
			'wedgeprops' : {'linewidth': 0},
			'textprops' : {'color':"white"}
		}
legendkwargs = {'frameon':False, 'ncol':1,'labelspacing':0.2} 

fig, axout, leg = piechartgrid(x='x',y='y', data=df, legendposition='left',subfigsize=(1,1), dpi=100,
				**{'pieargs':piekwargs,'legendargs':legendkwargs})
```

### Example 2

Distribution of diamond clarity as a function of price and weight (carat)

Data set is taken from: https://www.kaggle.com/shivam2503/diamonds
```
data = pd.read_csv('./diamonds.csv')

castep = 0.5
prstep = 3000.
data['carat']=np.floor(data['carat']/castep)
data['price']=np.floor(data['price']/prstep)

crlist = ['{:.1f} - {:.1f}'.format(i*castep,(i+1)*castep-0.01) for i in np.arange(data['carat'].min(),data['carat'].max()+1)]
prlist = ['{:5.0f} - {:5.0f}'.format(i*prstep,(i+1)*prstep-1) for i in np.arange(data['price'].min(),data['price'].max()+1)]

x=np.array([crlist[i] for i in data['carat'].astype(int)])
y=np.array([prlist[i] for i in data['price'].astype(int)])
df = pd.DataFrame(data={'cat. carat':x,'cat. price':y,'clarity':data['clarity']})
df = pd.get_dummies(df,columns=['clarity'],prefix='',prefix_sep='')

piekwargs = {'radius' :1.1, 'autopct' : "%.0f%%", 'pctdistance' : 0.7, 'shadow':True,
			'wedgeprops' : {'linewidth': 0},
			'textprops' : {'color':"white"}
		}
legendkwargs = {'frameon':False, 'ncol':1,'labelspacing':0.2, 'title':'clarity'} 

fig, axout, leg = piechartgrid(x='cat. carat',y='cat. price', data=df,subfigsize=(2,2), dpi=200,
				**{'pieargs':piekwargs,'legendargs':legendkwargs})

import os
fig.savefig(os.path.join('.','diamond_clarity.png'), dpi = 200, bbox_inches="tight")
``` 

For example, the labels can be changed afterwards using
```
axout.set_xlabel(r'$\alpha$')
axout.set_ylabel(r'$\beta$')
display(axout.figure)
```

To hide all percentages labels in the pie charts, set autopct `'autopct' : ""` or `'autopct' : "none"` in piekwargs.

# License

- piechartgrid is licensed under the MIT License:
  - [http://opensource.org/licenses/mit-license.html](http://opensource.org/licenses/mit-license.html)
- The piechartgrid documentation is licensed under the CC BY 3.0 License:
  - [http://creativecommons.org/licenses/by/3.0/](http://creativecommons.org/licenses/by/3.0/)

# Author

- GitHub: [https://github.com/smartens83](https://github.com/smartens83)
