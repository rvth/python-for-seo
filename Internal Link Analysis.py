#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import numpy as np
import requests
import urllib
import io


# In[3]:


#insert crawl csv 
data = ('/Users/rutheverett/Downloads/www-deepcrawl-com_12-10-2020_All_Pages_basic.csv')
#update to include columns you would like to include from csv 
columns = ['url', 'level', 'http_status_code', 'indexable', 'links_in_count', 'followed_links_in_count', 'links_out_count', 'deeprank', 'backlink_count', 'backlink_domain_count']
df = pd.read_csv(data , usecols=columns)


# In[7]:


#read first 10 rows
df.head(10)


# In[8]:


#set up segments 
segment_definitions = [
    [(r'\/blog\/'), 'Blog'],
    [(r'\/technical-seo-library\/'), 'Technical SEO Library'],
    [(r'\/hangout-library\/'), 'Hangout Library'],
    [(r'\/guides\/'), 'Guides'],
    [(r'\/case-studies\/'), 'Case Studies'],
    [(r'\/why-'), 'Solutions'],
    ]

use_segment_definitions = True

def get_segment(url):
    
    if use_segment_definitions == True:
        for segment_definition in segment_definitions:
            if re.findall(segment_definition[0], url):
                return segment_definition[1]
        return 'Other'

#apply segmentation to all URLs in dataframe 
df['segment'] = df['url'].apply(lambda x: get_segment(x))


# In[10]:


#create pivot table to get a count of internal links to each segment 
total_internal_links = pd.pivot_table(df, index='segment', values=['url', 'links_in_count', 'followed_links_in_count', 'links_out_count'], aggfunc={'url':len, 'links_in_count':np.sum, 'followed_links_in_count':np.sum, 'links_out_count':np.sum})
total_internal_links


# In[15]:


#create pivot table to get an of internal links to each segment 
average_internal_links = pd.pivot_table(df, index='segment', values=['url', 'links_in_count', 'followed_links_in_count', 'links_out_count'], aggfunc={'url':len, 'links_in_count':np.mean, 'followed_links_in_count':np.mean, 'links_out_count':np.mean})
average_internal_links['followed_links_in_count'] = (average_internal_links['followed_links_in_count']).apply('{:.1f}'.format)
average_internal_links['links_in_count'] = (average_internal_links['links_in_count']).apply('{:.1f}'.format)
average_internal_links['links_out_count'] = (average_internal_links['links_out_count']).apply('{:.1f}'.format)
average_internal_links


# In[17]:


#Additional step using Level and DeepRank to find averages for segments 
averages = pd.pivot_table(df, index='segment', values=['url', 'links_in_count', 'followed_links_in_count', 'links_out_count', 'deeprank', 'level'], aggfunc={'url':len, 'links_in_count':np.mean, 'followed_links_in_count':np.mean, 'links_out_count':np.mean, 'deeprank':np.mean, 'level':np.mean })
averages['followed_links_in_count'] = (averages['followed_links_in_count']).apply('{:.1f}'.format)
averages['links_in_count'] = (averages['links_in_count']).apply('{:.1f}'.format)
averages['links_out_count'] = (averages['links_out_count']).apply('{:.1f}'.format)
averages['deeprank'] = (averages['deeprank']).apply('{:.1f}'.format)
averages['level'] = (averages['level']).apply('{:.1f}'.format)
averages

