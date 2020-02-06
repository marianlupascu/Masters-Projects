# -*- coding: utf-8 -*-
"""Project2PML_V2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1raX4IUGx7qbpCLEePxZEIs7ixnqt60Oh

# **Suicide Rates Overview 1985 to 2016**
## Compares socio-economic info with suicide rates by year and country
"""

from google.colab import files, auth, drive
import numpy as np

# Mount to Google drive
drive.mount('/content/gdrive', force_remount=True)
data_dir_drive ='/content/gdrive/My Drive/Colab Notebooks/PML/Proj2/'

# Unzip dataset to /content
import time

start = time.time()

!unzip -u '/content/gdrive/My Drive/Colab Notebooks/PML/Proj2/suicide-rates-overview-1985-to-2016.zip' -d '/content/gdrive/My Drive/Colab Notebooks/PML/Proj2/'

print('Took', (time.time() - start), ' secundes to unzip')

! ls '/content/gdrive/My Drive/Colab Notebooks/PML/Proj2/'

"""# **Utils**
Some utility function to visualize the dataset and the model's predictions
"""

import pandas as pd 

pd.set_option("display.precision", 2)

# read data
df = pd.read_csv(data_dir_drive + 'master.csv') 

# Preview the first 5 lines 
df.head()

# print the shape of table
print(df.shape)

# print column names
print(df.columns)

# print same iformations about each column for table
print(df.info())

"""**HDI for year** care is the only column (exclusive feature) that have nulls

---

# **Data Analysis**
"""

# The describe method shows basic statistical characteristics of each 
# numerical feature (int64 and float64 types): number of non-missing values, 
# mean, standard deviation, range, median, 0.25 and 0.75 quartiles.
df.describe()

import matplotlib.pyplot as plt;
import numpy as np

data = df.to_numpy()
print(data)

"""![](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Sucide_rate.PNG/1280px-Sucide_rate.PNG)
Suicide rate per 100,000 people by country (1978-2009)
"""

# The distribution of suicides by countries
countries = data[:, 0]
objects = sorted(set(countries))
y_pos = np.arange(len(objects))
nr = []
for country in objects:
    nr.append(np.sum(np.dot((countries == country), data[:, 6]))) # population-related

fig=plt.figure(figsize=(15, 30), dpi= 80, facecolor='w', edgecolor='k')

order = np.argsort(nr)
nr = np.array(nr)[order]
objects = np.array(objects)[order]

plt.barh(y_pos, nr, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Number of suicides per country in 1985 - 2016')
plt.title('Countries distribution')

plt.show()

for idx in range(len(objects)):
    print(objects[idx] + ' have ' + str(nr[idx]) + ' suicides per 100000')

# The distribution of suicides by years
years = data[:, 1]
objects = sorted(set(years))
y_pos = np.arange(len(objects))
nr = []
for year in objects:
    nr.append(np.sum(np.dot((years == year), data[:, 4])))

fig=plt.figure(figsize=(15, 10), dpi= 80, facecolor='w', edgecolor='k')
plt.barh(y_pos, nr, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Number of suicides per year')
plt.title('Years distribution')

plt.show()

for idx in range(len(objects)):
    print(str(objects[idx]) + ' have ' + str(nr[idx]) + ' suicides')

# The distribution of suicides by sexes
sexes = data[:, 2]
objects = sorted(set(sexes))
y_pos = np.arange(len(objects))
nr = []
for sex in objects:
    nr.append(np.sum(np.dot((sexes == sex), data[:, 4])))

plt.barh(y_pos, nr, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Number of suicides per sex')
plt.title('Sexes distribution')

plt.show()

for idx in range(len(objects)):
    print(objects[idx] + ' have ' + str(nr[idx]) + ' suicides')

# The distribution of suicides by age categories
ages = data[:, 3]
objects = sorted(set(ages))
y_pos = np.arange(len(objects))
nr = []
for age in objects:
    nr.append(np.sum(np.dot((ages == age), data[:, 4])))

order = np.argsort(nr)
nr = np.array(nr)[order]
objects = np.array(objects)[order]

plt.barh(y_pos, nr, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Number of suicides per age')
plt.title('Ages distribution')

plt.show()

for idx in range(len(objects)):
    print(objects[idx] + ' have ' + str(nr[idx]) + ' suicides')

# The distribution of suicides by generation
gens = data[:, 11]
objects = sorted(set(gens))
y_pos = np.arange(len(objects))
nr = []
for gen in objects:
    nr.append(np.sum(np.dot((gens == gen), data[:, 4])))

order = np.argsort(nr)
nr = np.array(nr)[order]
objects = np.array(objects)[order]

plt.barh(y_pos, nr, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Number of suicides per generation')
plt.title('Generation distribution')

plt.show()

for idx in range(len(objects)):
    print(objects[idx] + ' have ' + str(nr[idx]) + ' suicides')

"""![](https://upload.wikimedia.org/wikipedia/commons/a/a4/Income_groups_2014-2016_by_GNI_per_capita.png)

Countries by income group
"""

# The distribution of suicides by GDP per capita per years
years = data[:, 1]
objects = sorted(set(years))
y_pos = np.arange(len(objects))
nr = []
for year in objects:
    print(year)
    GDPs = data[(years == year), 10]
    suicides = data[(years == year), 6]
    plt.hist(GDPs, weights = suicides, bins = 5)
    plt.show()

"""![](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/CountriesByGDPPerCapitaNominal2018.png/1280px-CountriesByGDPPerCapitaNominal2018.png)

## **Columns redundancy**
"""

df.head()

# suicides_no * 100000 / population	== suicides/100k
a = np.divide(data[:, 4] * 100000, data[:, 5])
a = a.astype(float)
a = np.around(a, decimals=2)

print(a.shape - np.sum(a == data[:, 6]))

for i in range(len(data)):
    a = np.divide(data[i, 4] * 100000, data[i, 5])
    a = a.astype(float)
    a = np.around(a, decimals=2)
    if a != data[i, 6]:
        print(data[i])
        print(abs(a - data[i, 6]))

country_years = sorted(set(data[:, 7]))
global_data = [] # macro data about each country per year

for country_year in country_years:
    population = 0 #population per country per year
    suicides = 0 #num of suicides per country per year
    for line in data:
        if line[7] == country_year:
            population += line[5]
            suicides += line[4]

    country = 0
    year = 0
    HDI_for_year = 0
    gdp_for_year = 0
    gdp_per_capita = 0

    for line in data:
        if line[7] == country_year:
            country = line[0]
            year = line[1]
            HDI_for_year = line[8]
            gdp_for_year = line[9]
            gdp_per_capita = line[10]
            break

    global_line = [country, 
                   year,
                   suicides, 
                   population, 
                   country_year, 
                   HDI_for_year, 
                   int(gdp_for_year.replace(',', '')), 
                   gdp_per_capita]
    global_data.append(global_line)

global_data = np.asarray(global_data, dtype=object)

a = np.rint(np.divide(np.asarray(global_data[:, 6], dtype=int),
                      np.asarray(global_data[:, 3], dtype=int))) - np.asarray(global_data[:, 7], dtype=int)
a = np.abs(a) # GDP / (GDP/capita) - population

print(str(np.sum(a > 0) * 100 / a.shape[0]) + '%')

for i in range(len(global_data)):
    a = np.rint(np.divide(np.asarray(global_data[i, 6], dtype=int),
                      np.asarray(global_data[i, 3], dtype=int))) - np.asarray(global_data[i, 7], dtype=int)

    if a != 0:
        print(global_data[i])
        print(a)

"""## **Extrapolates missing values for HDI**
![](https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/2019_UN_Human_Development_Report.svg/1280px-2019_UN_Human_Development_Report.svg.png)
"""

from scipy import interpolate

countries = data[:, 0]
countries = sorted(set(countries))

years = data[:, 1]
years = sorted(set(years))

HDI_for_year_mean = []
global_data_filled = global_data.copy()


for year in years:
    x = global_data[global_data[:, 1] == year,5]
    x = np.array(x, dtype=float)
    x = x[~np.isnan(x)]
    HDI_for_year_mean.append(np.mean(x))

idx_not_nan = np.argwhere(~np.isnan(np.asarray(HDI_for_year_mean, dtype=float)))[:, 0] 
HDIinterp = interpolate.interp1d(np.take(years, idx_not_nan), np.take(HDI_for_year_mean, idx_not_nan), fill_value="extrapolate", kind="linear")
HDI_for_year_mean = HDIinterp(years)

for country in countries:
    print(country)
    x = global_data[global_data[:, 0] == country, 1]
    y = global_data[global_data[:, 0] == country, 5]
    HDI_inferred = []

    idx_not_nan = np.argwhere(~np.isnan(np.asarray(y, dtype=float)))[:, 0] 

    plt.plot()
    if idx_not_nan.shape[0] == 0:
        print(x)
        print(y)
        z = HDI_for_year_mean.take(np.array(x, dtype=int)-1985)
        HDI_inferred = z
        print(z)
        plt.plot(x, z)
    elif idx_not_nan.shape[0] == 1:
        print(x)
        print(y)
        if y[idx_not_nan[0]] < HDI_for_year_mean[x[idx_not_nan[0]]-1985]:
            z = HDI_for_year_mean.take(np.array(x, dtype=int)-1985) - abs(y[idx_not_nan[0]] - HDI_for_year_mean[x[idx_not_nan[0]]-1985])
            HDI_inferred = z
            print(z)
            plt.plot(x, z)
        else:
            z = HDI_for_year_mean.take(np.array(x, dtype=int)-1985) - abs(y[idx_not_nan[0]] + HDI_for_year_mean[x[idx_not_nan[0]]-1985])
            HDI_inferred = z
            print(z)
            plt.plot(x, z)
    else:
        f = interpolate.interp1d(np.take(x, idx_not_nan), np.take(y, idx_not_nan), fill_value="extrapolate", kind="linear")
        z = f(np.array(x, dtype=float))
        HDI_inferred = z
        plt.plot(x, z)
    plt.plot(np.take(x, idx_not_nan), np.take(y, idx_not_nan), 'ro')
    plt.show()

    for year_idx in range(len(x)):
        idx = np.where(np.logical_and(global_data[:, 0] == country, global_data[:, 1] == x[year_idx]))[0][0]
        global_data_filled[idx, 5] = round(HDI_inferred[year_idx], 2)

print(global_data_filled[:50, :])

data_fill = data.copy()

countries = data[:, 0]
countries = sorted(set(countries))

years = data[:, 1]
years = sorted(set(years))

for idx, country_years in enumerate(global_data_filled[:, 4]):
    data_fill[data_fill[:, 7] == country_years, 8] = global_data_filled[idx, 5]
    data_fill[data_fill[:, 7] == country_years, 9] = global_data_filled[idx, 6]

print(data_fill[:50, :])

# The distribution of suicides by HDI per years
years = data_fill[:, 1]
objects = sorted(set(years))
y_pos = np.arange(len(objects))
nr = []
for year in objects:
    print(year)
    HDIs = data_fill[(years == year), 8]
    suicides = data_fill[(years == year), 4]
    plt.hist(HDIs, weights = suicides)
    plt.show()

# Creating pandas dataframe from numpy array
columns = df.columns
dataset = pd.DataFrame({columns[i]: data_fill[:, i] for i in range(len(columns))})

dataset

# print same iformations about each column for table
print(dataset.info())

dataset.describe()

""".

# **Apriori about suicide rate**
"""

rate_dict = {data_fill[x, 7]: data_fill[x, 6] for x in range(data_fill.shape[0])}
rate = data_fill[:, 6]

print('Min: \t\t' + str(np.amin(rate)))
print('25%: \t\t' + str(np.percentile(rate, 25)))
print('50%: \t\t' + str(np.percentile(rate, 50)))
print('75%: \t\t' + str(np.percentile(rate, 75)))
print('Max: \t\t' + str(np.amax(rate)))
print('Mean : \t\t' + str(np.mean(rate)))
print('Std : \t\t' + str(np.std(rate)))
print('Var : \t\t' + str(np.var(rate)))

y1 = np.where(rate<np.percentile(rate, 25), 1, 0)
y2 = np.where(np.logical_and(rate>=np.percentile(rate, 25), rate<np.percentile(rate, 50)), 2, 0)
y3 = np.where(np.logical_and(rate>=np.percentile(rate, 50), rate<np.percentile(rate, 75)), 3, 0)
y4 = np.where(rate>=np.percentile(rate, 75), 4, 0)

Y = y1 + y2 + y3 + y4 - 1

print(y1.sum())
print((y2 != 0).sum())
print((y3 != 0).sum())
print((y4 != 0).sum())

dataset2 = dataset.copy()

dataset2

# categorical feature
for line in range(dataset2.shape[0]):
    if dataset2['sex'][line] == 'male':
        dataset2['sex'][line] = 0
    else:
        dataset2['sex'][line] = 1

dataset2

objects = sorted(set(dataset2['age']))
objects

# ordinal feature
years_dict = {
    '15-24 years' : 0,
    '25-34 years' : 1,
    '35-54 years' : 2,
    '5-14 years' : 3,
    '55-74 years' : 4,
    '75+ years' : 5
}
for line in range(dataset2.shape[0]):
    dataset2['age'][line] = years_dict[dataset2['age'][line]]

dataset2

objects = sorted(set(dataset2['generation']))
objects

# ordinal feature
generation_dict = {
    'Boomers' : 2,         # 1946 - 1964
    'G.I. Generation' : 0, # 1901 - 1927
    'Generation X' : 3,    # 1961 - 1981
    'Generation Z' : 5,    # 1995 - 
    'Millenials' : 4,      # 1981 - 1996
    'Silent' : 1           # 1928 - 1945
}
for line in range(dataset2.shape[0]):
    dataset2['generation'][line] = generation_dict[dataset2['generation'][line]]

dataset2

dataset2.columns

dataset3 = dataset2.drop(columns=['suicides_no', 'population', 'country-year', ' gdp_for_year ($) '])

dataset3

columns3 = dataset3.columns
columns3 = list(columns3)

dataset4 = pd.get_dummies(dataset3, columns=['country'])

dataset4

dataset4.insert(0, 'country', dataset3['country'][:])

dataset4

X = dataset4.to_numpy()

"""### **Imports**"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import seaborn as sns; sns.set(style='white')

from sklearn import decomposition
from sklearn import datasets
from mpl_toolkits.mplot3d import Axes3D

from pylab import rcParams
rcParams['figure.figsize'] = 12, 12

"""### **Utility plotting functions**"""

COLORS = ['tab:blue', 'tab:green', 'tab:orange', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:olive', 'tab:cyan', 'tab:gray']
MARKERS = ['o', 'v', 's', '<', '>', '8', '^', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']

def plot2d(X, y_pred, y_true, mode=None, centroids=None):
    transformer = None
    X_r = X
    
    if mode is not None:
        transformer = mode(n_components=2)
        X_r = transformer.fit_transform(X)

    assert X_r.shape[1] == 2, 'plot2d only works with 2-dimensional data'


    plt.grid()
    for ix, iyp, iyt in zip(X_r, y_pred, y_true):
        plt.plot(ix[0], ix[1], 
                    c=COLORS[iyp], 
                    marker=MARKERS[iyt])
        
    if centroids is not None:
        C_r = centroids
        if transformer is not None:
            C_r = transformer.fit_transform(centroids)
        for cx in C_r:
            plt.plot(cx[0], cx[1], 
                        marker=MARKERS[-1], 
                        markersize=10,
                        c='red')

    plt.show()

def plot3d(X, y_pred, y_true, mode=None, centroids=None):
    transformer = None
    X_r = X
    if mode is not None:
        transformer = mode(n_components=3)
        X_r = transformer.fit_transform(X)

    assert X_r.shape[1] == 3, 'plot2d only works with 3-dimensional data'

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.elev = 30
    ax.azim = 120

    for ix, iyp, iyt in zip(X_r, y_pred, y_true):
        ax.plot(xs=[ix[0]], ys=[ix[1]], zs=[ix[2]], zdir='z',
                    c=COLORS[iyp], 
                    marker=MARKERS[iyt])
        
    if centroids is not None:
        C_r = centroids
        if transformer is not None:
            C_r = transformer.fit_transform(centroids)
        for cx in C_r:
            ax.plot(xs=[cx[0]], ys=[cx[1]], zs=[cx[2]], zdir='z',
                        marker=MARKERS[-1], 
                        markersize=10,
                        c='red')
    plt.show()

plot2d(X[(X[:, 0] == 'Romania'), 1:], Y[(X[:, 0] == 'Romania')], Y[(X[:, 0] == 'Romania')], PCA)

plot2d(X[(X[:, 0] == 'Lithuania'), 1:], Y[(X[:, 0] == 'Lithuania')], Y[(X[:, 0] == 'Lithuania')], PCA)

rperm = np.random.permutation(X.shape[0])
plot2d(X[rperm[:5000], 1:], Y[rperm[:5000]], Y[rperm[:5000]], PCA)

plot3d(X[(X[:, 0] == 'Romania'), 1:], Y[(X[:, 0] == 'Romania')], Y[(X[:, 0] == 'Romania')], PCA)

plot3d(X[(X[:, 0] == 'Lithuania'), 1:], Y[(X[:, 0] == 'Lithuania')], Y[(X[:, 0] == 'Lithuania')], PCA)

rperm = np.random.permutation(X.shape[0])
plot3d(X[rperm[:5000], 1:], Y[rperm[:5000]], Y[rperm[:5000]], PCA)

"""# **K-means**"""

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=4, random_state=42).fit(X[:, 1:])

for country in countries:
    lines = (X[:, 0] == country)
    print(country)
    labels = kmeans.labels_[lines]
    print('0: '+ str(np.sum(labels == 0)) + '\t\t1: '+ str(np.sum(labels == 1)) + '\t\t2: '+ str(np.sum(labels == 2)) + '\t\t3: '+ str(np.sum(labels == 3)))

rperm = np.random.permutation(X.shape[0])
plot3d(X[rperm[:5000], 1:], kmeans.labels_[rperm[:5000]], kmeans.labels_[rperm[:5000]], mode=TSNE)

import sklearn
sklearn.metrics.silhouette_score(X[:, 1:], kmeans.labels_)

maximum = sklearn.metrics.silhouette_score(X[:, 1:], kmeans.labels_)
optimum = 4
labels = kmeans.labels_
scores = []
for i in range(2, 20):
    kmeans = KMeans(n_clusters=i, random_state=42).fit(X[:, 1:])
    silhouette_score = sklearn.metrics.silhouette_score(X[:, 1:], kmeans.labels_)
    if silhouette_score > maximum:
        maximum = silhouette_score
        optimum = i
        labels = kmeans.labels_
    scores.append(silhouette_score)

plt.plot(range(2, 20), scores)

print(optimum)
print(maximum)

from yellowbrick.cluster import SilhouetteVisualizer

# Instantiate the clustering model and visualizer
model = KMeans()
visualizer = SilhouetteVisualizer(model, k=(2,21))

visualizer.fit(X[:, 1:])        # Fit the data to the visualizer

from yellowbrick.cluster import KElbowVisualizer

# Instantiate the clustering model and visualizer
model = KMeans()
visualizer = KElbowVisualizer(model, k=(2,21))

visualizer.fit(X[:, 1:])        # Fit the data to the visualizer

C = 2
kmeans = KMeans(n_clusters=C, random_state=42).fit(X[:, 1:])

rperm = np.random.permutation(X.shape[0])
plot3d(X[rperm[:5000], 1:], kmeans.labels_[rperm[:5000]], kmeans.labels_[rperm[:5000]], mode=TSNE)

sklearn.metrics.silhouette_score(X[:, 1:], kmeans.labels_)

sklearn.metrics.calinski_harabasz_score(X[:, 1:], kmeans.labels_)

sklearn.metrics.davies_bouldin_score(X[:, 1:], kmeans.labels_)

ans = {x : [] for x in range(C)}
for country in countries:
    lines = (X[:, 0] == country)
    labels = kmeans.labels_[lines]
    ans[np.argmax([np.sum(labels == x)/np.sum(kmeans.labels_ == x) for x in range (C)])].append(country)

ans

! pip install pycountry

import pycountry

def make_preprocessing_for_countries_plot(model_labels = None):
    countries_df = []
    inv_ans = []
    iso_alpha = []

    C = len(set(model_labels)) - (1 if -1 in model_labels else 0)

    for country in countries:
        lines = (X[:, 0] == country)
        labels = model_labels[lines]
        try:
            a = pycountry.countries.search_fuzzy(country)[0]
            if len(a.alpha_3) != 3:
                break
            countries_df.append(country)
            lb = np.argmax([np.sum(labels == x)/np.sum(model_labels == x) for x in range (C)])
            inv_ans.append(lb)
            iso_alpha.append(a.alpha_3)
        except:
            pass

    return pd.DataFrame({'country': countries_df, 'label': inv_ans, 'iso_alpha': iso_alpha})

dataset_plot = make_preprocessing_for_countries_plot(kmeans.labels_)

import plotly.express as px

fig = px.choropleth(dataset_plot, locations="iso_alpha",
                    color="label", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
fig.show()

C = 17
kmeans = KMeans(n_clusters=C, random_state=42).fit(X[:, 1:])

sklearn.metrics.silhouette_score(X[:, 1:], kmeans.labels_)

sklearn.metrics.calinski_harabasz_score(X[:, 1:], kmeans.labels_)

sklearn.metrics.davies_bouldin_score(X[:, 1:], kmeans.labels_)

ans = {x : [] for x in range(C)}
for country in countries:
    lines = (X[:, 0] == country)
    labels = kmeans.labels_[lines]
    ans[np.argmax([np.sum(labels == x)/np.sum(kmeans.labels_ == x) for x in range (C)])].append(country)

ans

dataset_plot = make_preprocessing_for_countries_plot(kmeans.labels_)

import plotly.express as px

fig = px.choropleth(dataset_plot, locations="iso_alpha",
                    color="label", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
fig.show()

"""# **DBSCAN**"""

from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=1000, min_samples=50).fit(X[:, 1:])

rperm = np.random.permutation(X.shape[0])
plot3d(X[rperm[:5000], 1:], dbscan.labels_[rperm[:5000]], Y[rperm[:5000]], mode=PCA)

# Number of clusters in labels, ignoring noise if present.
labels = dbscan.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print(n_clusters_)
print(n_noise_)

sklearn.metrics.silhouette_score(X[:, 1:], dbscan.labels_)

for country in countries:
    lines = (X[:, 0] == country)
    print(country)
    labels = dbscan.labels_[lines]
    print('0: '+ str(np.sum(labels == 0)) + '\t\t1: '+ str(np.sum(labels == 1)) + '\t\t2: '+ str(np.sum(labels == 2)) + '\t\t3: '+ str(np.sum(labels == 3)))

maximum = sklearn.metrics.silhouette_score(X[:, 1:], dbscan.labels_)
optimum = 4
model = dbscan
eps=1000
min_samples=50
scores = []
epss = []
min_sampless = []
for eps_idx in range(1000, 3000, 250):
    for min_samples_idx in range(10, 50, 5):
        dbscan = DBSCAN(eps=eps_idx, min_samples=min_samples_idx).fit(X[:, 1:])
        if len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0) <= 1:
            continue
        silhouette_score = sklearn.metrics.silhouette_score(X[:, 1:], dbscan.labels_)
        if silhouette_score > maximum:
            maximum = silhouette_score
            optimum = len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0)
            model = dbscan
            eps=eps_idx
            min_samples=min_samples_idx
        scores.append(silhouette_score)
        epss.append(eps_idx)
        min_sampless.append(min_samples_idx)

print(optimum)
print(maximum)
print(eps)
print(min_samples)

sklearn.metrics.calinski_harabasz_score(X[:, 1:], model.labels_)

sklearn.metrics.davies_bouldin_score(X[:, 1:], model.labels_)

# Number of clusters in labels, ignoring noise if present.
labels = model.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print(n_clusters_)
print(n_noise_)

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


ax.scatter(epss, min_sampless, scores)

ax.set_xlabel('eps')
ax.set_ylabel('min_samples')
ax.set_zlabel('silhouette_score')

plt.show()

ans = {x : [] for x in range(optimum)}
for country in countries:
    lines = (X[:, 0] == country)
    labels = model.labels_[lines]
    ans[np.argmax([np.sum(labels == x)/np.sum(model.labels_ == x) for x in range (optimum)])].append(country)

ans

dataset_plot = make_preprocessing_for_countries_plot(model.labels_)

import plotly.express as px

fig = px.choropleth(dataset_plot, locations="iso_alpha",
                    color="label", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
fig.show()

"""# **Hierarchical Clustering**"""

from scipy.cluster import hierarchy as hc

dataset3.columns

# Perform hierarchical clustering using single linkage
Z = hc.linkage(dataset3[dataset3.columns[1:]], 'single')

fig = plt.figure(figsize=(25, 15))
dn = hc.dendrogram(Z, labels=dataset3['country'].values, truncate_mode='lastp', p = 30)
plt.show()

# Perform hierarchical clustering using Ward linkage
Z = hc.linkage(dataset3[dataset3.columns[1:]], 'ward', metric='euclidean')

fig = plt.figure(figsize=(25, 15))
dn = hc.dendrogram(Z, labels=dataset3['country'].values, truncate_mode='lastp', p = 30)
plt.show()

fig = plt.figure(figsize=(300, 30))
dn = hc.dendrogram(Z, labels=dataset3['country'].values, truncate_mode='level', p = 9, leaf_font_size = 11, leaf_rotation = 45)
plt.show()

C = 4
clusters = hc.fcluster(Z, t=C, criterion='maxclust') - 1

maximum = sklearn.metrics.silhouette_score(X[:, 1:], clusters)
optimum = 4
labels = clusters
scores = []
for i in range(2, 20):
    clusters = hc.fcluster(Z, t=i, criterion='maxclust') - 1
    silhouette_score = sklearn.metrics.silhouette_score(X[:, 1:], clusters)
    if silhouette_score > maximum:
        maximum = silhouette_score
        optimum = i
        labels = clusters
    scores.append(silhouette_score)

plt.plot(range(2, 20), scores)

print(optimum)
print(maximum)

clusters = hc.fcluster(Z, t=9, criterion='maxclust') - 1

rperm = np.random.permutation(X.shape[0])
plot3d(X[rperm[:5000], 1:], clusters[rperm[:5000]], clusters[rperm[:5000]], mode=PCA)

rperm = np.random.permutation(X.shape[0])
plot3d(X[rperm[:5000], 1:], clusters[rperm[:5000]], clusters[rperm[:5000]], mode=TSNE)

sklearn.metrics.silhouette_score(X[:, 1:], clusters)

sklearn.metrics.calinski_harabasz_score(X[:, 1:], clusters)

sklearn.metrics.davies_bouldin_score(X[:, 1:], clusters)

sklearn.metrics.cluster.contingency_matrix(X[:, 0], clusters)

ans = {x : [] for x in range(8)}
for country in countries:
    lines = (X[:, 0] == country)
    labels = clusters[lines]
    ans[np.argmax([np.sum(labels == x)/np.sum(clusters == x) for x in range (8)])].append(country)

ans

dataset_plot = make_preprocessing_for_countries_plot(clusters)

import plotly.express as px

fig = px.choropleth(dataset_plot, locations="iso_alpha",
                    color="label", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
fig.show()



# Perform hierarchical clustering using centroid linkage
Z = hc.linkage(dataset3[dataset3.columns[1:]], 'centroid', metric='euclidean')

C = 4
clusters = hc.fcluster(Z, t=C, criterion='maxclust') - 1

maximum = sklearn.metrics.silhouette_score(X[:, 1:], clusters)
optimum = 4
labels = clusters
scores = []
for i in range(2, 20):
    clusters = hc.fcluster(Z, t=i, criterion='maxclust') - 1
    silhouette_score = sklearn.metrics.silhouette_score(X[:, 1:], clusters)
    if silhouette_score > maximum:
        maximum = silhouette_score
        optimum = i
        labels = clusters
    scores.append(silhouette_score)

plt.plot(range(2, 20), scores)

print(optimum)
print(maximum)

clusters = hc.fcluster(Z, t=14, criterion='maxclust') - 1

sklearn.metrics.silhouette_score(X[:, 1:], clusters)

sklearn.metrics.calinski_harabasz_score(X[:, 1:], clusters)

sklearn.metrics.davies_bouldin_score(X[:, 1:], clusters)

sklearn.metrics.cluster.contingency_matrix(X[:, 0], clusters)

ans = {x : [] for x in range(14)}
for country in countries:
    lines = (X[:, 0] == country)
    labels = clusters[lines]
    ans[np.argmax([np.sum(labels == x)/np.sum(clusters == x) for x in range (14)])].append(country)

ans

dataset_plot = make_preprocessing_for_countries_plot(clusters)

import plotly.express as px

fig = px.choropleth(dataset_plot, locations="iso_alpha",
                    color="label", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
fig.show()

! pip install fastcluster

import fastcluster
import scipy
Z = fastcluster.linkage(dataset3[dataset3.columns[1:]], method="ward")

fig = plt.figure(figsize=(25, 15))
dn = hc.dendrogram(Z, labels=dataset3['country'].values, truncate_mode='lastp', p = 30)
plt.show()