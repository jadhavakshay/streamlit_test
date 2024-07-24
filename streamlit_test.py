
import pandas as pd
import numpy as np
import scipy
import plotly.figure_factory as ff
import streamlit as st

# Title widget
st.title('Streamlit')
st.text("Function test")

# radio widget to take inputs from mulitple options
genre = st.radio(
    "What's your favorite movie genre",
    ('Comedy', 'Drama', 'Documentary'))

if genre == 'Comedy':
    st.write('You selected comedy.')
elif genre == 'Drama':
    st.write('You selected drama.')
elif genre == 'Documentary':
    st.write('You selected documentary.')

# Usage of multiselect widget
import streamlit as st

options = st.multiselect(
    'What are your favorite colors',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow'])

st.write('You selected:', options)

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

df = pd.DataFrame(
   np.random.randn(50, 10),
   columns=('col %d' % i for i in range(10)))

st.dataframe(df)

uploaded_file = st.file_uploader("Choose a File", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = uploaded_file.read()
    st.image(image, caption='uploaded image', use_column_width=True)
