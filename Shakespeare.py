import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud, STOPWORDS
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords 
nltk.download('punkt')
st.markdown('''
# Analyzing Shakespeare Texts
''')

# Create a dictionary (not a list)
books = {" ":" ","A Mid Summer Night's Dream":"summer.txt",
         "The Merchant of Venice":"merchant.txt",
         "Romeo and Juliet":"romeo.txt"}

# Sidebar
st.sidebar.header('Word Cloud Settings')
word_max = st.sidebar.slider("Max Words",min_value=10, max_value=200, value=100, step=10)
large_size= st.sidebar.slider("Size of Largest Word",min_value=50, max_value=350, value=50, step=10)
Picture_size= st.sidebar.slider("Size of Image",min_value=100, max_value=800, value=100, step=25)
random_state= st.sidebar.slider("Random State",min_value=5, max_value=100, value=50, step=10)
remove_stopwords = st.sidebar.checkbox("Remove Stop Words?",value=True)



st.sidebar.header('Word Count Settings')
min_cnt_words = st.sidebar.slider("Minimum Count of Words",min_value=5, max_value=100, value=50, step=10)

## Select text files
image = st.selectbox("Choose a text file", books.keys())

## Get the value
image = books.get(image)


if image != " ":
    stop_words = []
    raw_text = open(image,"r").read().lower()
    nltk_stop_words = stopwords.words('english')

    if remove_stopwords:
        stop_words = set(nltk_stop_words)
        stop_words.update(['us', 'one', 'though','will', 'said', 'now', 'well', 'man', 'may',
        'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
        'put', 'seem', 'asked', 'made', 'half', 'much',
        'certainly', 'might', 'came','thou'])
        # These are all lowercase

tab1, tab2, tab3 = st.tabs(['Word Cloud', 'Bar Chart', 'View Text'])

with tab1:
        if image != " ":
            if remove_stopwords: 
                cloud = WordCloud(background_color = "white", max_words = word_max, max_font_size=large_size, 
                                  stopwords = stop_words, random_state=random_state)
            else:
                cloud = WordCloud(background_color = "white", 
                           max_words = word_max, 
                            max_font_size=large_size, 
                            random_state=random_state)
            
            wc = cloud.generate(raw_text)
            word_cloud = cloud.to_file('wordcloud.png')  
            st.image(wc.to_array(), width = Picture_size)
with tab2:
    if image != " ":
         st.write('Bar chart')
         tokens = nltk.word_tokenize(raw_text)
         tokens = [t for t in tokens if t.isalpha()]
         sw_remove = [w for w in tokens if not w.lower() in stop_words]
         if remove_stopwords:
                  frequency = nltk.FreqDist(sw_remove)
                  freq_df = pd.DataFrame(frequency.items(),columns=['word','count'])
                  sorted_data = freq_df.sort_values("count", ascending=False)
                  df = sorted_data[ sorted_data.iloc[:,1]>= min_cnt_words ]
                  bars = alt.Chart(df).mark_bar().encode(
                  x='count',
                  y=alt.Y('word:N', sort='-x')
                  )
                  st.altair_chart(bars, use_container_width=True)
        
         else:
                  frequency = nltk.FreqDist(tokens)
                  freq_df = pd.DataFrame(frequency.items(),columns=['word','count'])
                  sorted_data = freq_df.sort_values("count", ascending=False)
                  df = sorted_data[ sorted_data.iloc[:,1]>= min_cnt_words ]
             
                  bars = alt.Chart(df).mark_bar().encode(
                  x='count',
                  y=alt.Y('word:N', sort='-x')
                  )
                  st.altair_chart(bars, use_container_width=True)
        

with tab3:
    if image != " ":
        raw_text = open(image,"r").read().lower()
        st.write(raw_text)
