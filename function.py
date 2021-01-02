#Import modules
import pandas as pd
from ast import literal_eval
import numpy as np
import scipy
from scipy import sparse
from sklearn.feature_extraction.text import TfidfTransformer

#Creates a dict of brand matrix locations from a series of json objects each describing the top 20 brands that the devices that stopped in an area visited in the same period as the stop in the area.
#SafeGraph brands as keys and matrix locations as values
def brand_locations(sgbs):
  sgbs = sgbs.apply(literal_eval)
  sgbd = {}
  i = 0
  for brand in set([y for x in sgbs for y in x]):
    sgbd[brand]=i
    i+=1
  return sgbd
  
#Creates a dict of geography matrix locations from a series of unique strings each naming a geography of study.
#SafeGraph geographies as keys and matrix locations as values
def geo_locations(sggs):
  sggd = {}
  i = 0
  for area in set(sggs):
    sggd[area]=i
    i+=1
  return sggd
  
#Creates a matrix representation of SafeGraph top same-period brand percentages in a collection of SafeGraph geographies (provided as a dataframe), analagous to the output of sklearn.feature_extraction.text.CountVectorizer for token counts in a collection of text documents. 
#SafeGraph geography indices as rows and SafeGraph brand indices as columns
def sgPercentVectorizer(df, gidxs, bidxs, period):
  count_vector_dense = np.zeros((len(gidxs), len(bidxs)))
  
  for row in df.itertuples():
    top_same_period_brand = literal_eval(row[2])
    area = row[1]
    for key,val in top_same_period_brand.items():
      count_vector_dense[gidxs[area], bidxs[key]] = val
      
  return sparse.csr_matrix(count_vector_dense)
  
#Calculates a matrix of tf-idf scores corresponding to a matrix of word counts
##SafeGraph geography indices as rows and SafeGraph brand indices as columns
def sgTfIdfCalculator(sgm):
  tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True, norm=None)
  tfidf_transformer.fit(sgm)
  return tfidf_transformer.transform(sgm)
  
#Transforms SafeGraph brand data into Tf-Idf metrics according to user specifications
#       sgdf = a Neighborhood Patterns release (dataframe)
#       period = {'day', 'month'}
#       cohort = {2-digit state, 5-digit county, 'us'}
def brand_transformer(sgdf, period, cohort):
  transformed ={'gidxs': None, 'bidxs': None, 'tfidf': None, 'period': None, 'cohort': None, 'date': None}
  transformed['date'] = sgdf['date_range_start'][0][:7]
  
  if period == 'day':
    columns = ['area', 'top_same_day_brand']
    transformed['period'] = period
  else:
    columns = ['area', 'top_same_month_brand']
    transformed['period'] = 'month'

  try:
    int(cohort)
    sgdf = sgdf[columns][sgdf['area'].apply(lambda x: x[:len(cohort)]==cohort)]
    transformed['cohort'] = cohort
  except:
    contiguous = ['01', '04', '05', '06', '08', '09', '10', '11', '12', '13', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56']
    sgdf = sgdf[columns][sgdf['area'].apply(lambda x: x[:2] in contiguous)]
    transformed['cohort']='us'    

  transformed['gidxs'] = geo_locations(sgdf.iloc[:,0])
  transformed['bidxs'] = brand_locations(sgdf.iloc[:,1])
  
  count_vector = sgPercentVectorizer(sgdf, transformed['gidxs'], transformed['bidxs'], transformed['period'])
  transformed['tfidf'] = sgTfIdfCalculator(count_vector)

  return transformed