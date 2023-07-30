from cProfile import label
import streamlit as st
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt



DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

st.set_page_config(layout='wide')

if st.checkbox('Clique aqui para parar o carregamento de dados'):
    st.stop()


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data = load_data(10000)


progress_bar = st.progress(0)
status_text = st.empty()
for i in range(100):

    progress_bar.progress(i + 1)
    time.sleep(0.1)

st.success('Dados carregados com sucesso!', icon="✅")



if st.checkbox('Mostrar tabela de dados'):
    st.subheader('Tabela de dados')
    st.write(data)

st.markdown('---')

st.write('Histograma dos dados')
time.sleep(2)
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

st.markdown('---')

st.area_chart(data[DATE_COLUMN])


st.markdown('---')

data1 = data[['date/time']]
fig, ax = plt.subplots()
plt.xticks(rotation=90)
ax.hist(data1, bins=20)

st.pyplot(fig)

st.markdown('---')

st.line_chart(data1)

st.markdown('---')


st.write('Dados plotados no mapa')
st.map(data)

st.markdown('---')

hour_to_filter = st.slider('hora', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)


st.markdown('---')


st.table(data.head(5))

#baixar o df usado no codigo
@st.cache_data
def convert_df(data):
    
    return data.to_csv().encode('utf-8')

csv = convert_df(data)
st.download_button(
    label="Baixar DataFrame",
    data=csv,
    file_name='DataFrame.csv',
    mime='text/csv',
)