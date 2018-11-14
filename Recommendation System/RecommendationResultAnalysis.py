
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# # Load data into pandas

# In[162]:


#read csv
recco_data = pd.read_csv("itemRecoWithNames.csv")


# In[163]:


recco_data


# # Load Movie Description Data

# In[144]:


movie_data = pd.read_csv("movie_db_yoda.csv")


# # Drop all other columns 

# In[145]:


columns_want = ["Movie ID", "Title"]
select = [x for x in movie_data.columns if x not in columns_want]
movie_data = movie_data.drop(select,axis = 1 )


# In[146]:


movie_data


# # Perform Table merge on Movie Title

# In[152]:


movie1DF = recco_data.merge(movie_data, left_on='Movie 1', right_on='Movie ID')
movie1DF = movie1DF.rename(index=str, columns={"Title": "Movie1 Title"})
movie1DF = movie1DF.drop(['Movie ID','Movie 1 Title'],axis = 1 )


# In[153]:


movie1DF


# In[154]:


movie2DF = movie1DF.merge(movie_data, left_on='Movie 2', right_on='Movie ID')
movie2DF = movie2DF.rename(index=str, columns={"Title": "Movie2 Title"})
movie2DF = movie2DF.drop(['Movie ID','Movie 2 Title'],axis = 1 )


# In[155]:


movie2DF


# # Sort and view Top 100 Similar Movies with high Similarity

# In[156]:


m2df = movie2DF.sort_values(by=['Similarity'],ascending=False)
m2df = m2df[['Movie 1', 'Movie1 Title', 'Movie 2', 'Movie2 Title','Similarity']]


# In[157]:


m2df.head(100)

