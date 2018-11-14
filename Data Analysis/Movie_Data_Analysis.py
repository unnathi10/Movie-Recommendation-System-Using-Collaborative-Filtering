
# coding: utf-8

# In[3]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
columns = ['UserID', 'Movie ID', 'Rating']
data = pd.read_csv("ydata-ymovies-user-movie-ratings-train-v1_0-txt.csv", names = columns)
movies = pd.read_csv("movie_db_yoda.csv")
data1 = data.iloc[1:]
data1.head(5)


# In[42]:


movie = movies[['Movie ID', 'Title', 'Genres']]
movie_data = pd.merge(data1, movie)
movie_data.head(6)


# In[156]:


top_movies = movie_data.Title.value_counts()[:10]
plt.figure(figsize=(12, 8))
pos = np.arange(len(top_movies))
plt.barh(pos, top_movies.values, color = 'purple');
plt.yticks(pos, top_movies.index);
plt.title('Most Rated Movies')
plt.ylabel('Title')


# # Get Most Rated Movies:

# In[157]:


top_movies


# In[158]:


plt.show()


# # Get Most Rated Genres:

# In[112]:


movie_data['Genre_Split'] = movie_data['Genres'].str.split('|')
movie_data.head()


# In[183]:


top_genres = []
for i in movie_data['Genre_Split']:
    if(isinstance(i, list)):
        for j in i:
            x = i.count(j)
            top_genres.append(x)


# In[7]:


top_genres = movie_data.Genres.value_counts()[:16]
top_genres = top_genres.drop(top_genres.index[2])
plt.figure(figsize=(12, 8))
pos = np.arange(len(top_genres))
plt.barh( pos, top_genres.values, color = 'indigo');
plt.yticks(pos,top_genres.index);
plt.title('Most Rated Genres')
plt.ylabel('Genre')


# In[8]:


top_genres.drop(top_genres.index[2])


# In[9]:


plt.show()


# # Get Top 10 Users Who Gave The Most Ratings:

# In[43]:


top_users = movie_data.UserID.value_counts()[:10]
plt.figure(figsize=(12, 8))
pos = np.arange(len(top_users))
plt.barh( pos, top_users.values, color = 'green');
plt.yticks(pos,top_users.index);
plt.title('Top 10 Users who gave the most ratings')
plt.ylabel('User ID')


# In[44]:


plt.show()


# In[45]:


top_users


# In[57]:


explode = (0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
plt.pie(top_users.values, explode = explode, autopct='%0.0f%%',shadow=True, startangle=130)
plt.legend(labels = top_users.index, loc = 'upper right')
plt.title("Top 10 Users who gave the most ratings")
plt.axis('equal')
plt.show()


# In[70]:


movie_data['genre_arr'] = movie_data['Genres'].str.split('|')
movie_data.head(5)


# In[1]:


genre = {'Adventure': 1117, 'Animation': 447, 'Children': 583, 'Drama': 3315, 'Fantasy': 654, 'Romance': 1545, 'Comedy': 4365, 'Action': 1545, 'Crime': 1100, 'Thriller': 1729, 'Horror': 877, 'Mystery': 543, 'Sci-Fi': 792, 'Documentary': 495, 'IMAX': 153, 'War': 367, 'Musical': 394, 'Western': 168, 'Film-Noir': 133, '(no genres listed)': 18}
genre


# In[23]:


genre.keys()


# In[95]:


explode = (0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
plt.pie(genre.values(), labels= genre.keys(),explode = explode,autopct='%0.1f%%', colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral'] )
plt.title("Most Rated Genre")
#plt.legend(, loc = 'right')
plt.axis('equal')
plt.show()


# In[43]:


movie_data.head()


# In[44]:


mdata = movie_data[['Title','Genres']]


# In[45]:


mdata.head()


# In[61]:


m =  mdata['Genres'].value_counts()[:20]


# In[62]:


m


# # Get Number of Movies in Each Genre:

# In[99]:


genre = m
x = list(range(len(genre)))
plt.xticks(x, genre.index, rotation=90)
plt.bar(x, genre.values, color = 'indigo')
plt.xlabel("Number of genres")
plt.ylabel("Number of movies")
plt.title('Number of Movies in each Genre')
plt.grid()
plt.plot()
plt.show()


# # Get Number of Movies Per Rating:

# In[101]:


m =  movie_data['Rating'].value_counts()
m.head()


# In[104]:


re = m
plt.figure(figsize=(12, 8))
pos = np.arange(len(re))
plt.barh(pos, re.values, color = 'violet');
plt.yticks(pos, re.index);
plt.title('Number of Movies per Rating')
plt.xlabel('Number of Movies')
plt.ylabel('Rating')


# In[105]:


plt.show()

