import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from io import StringIO

st.title("Streamlit")

data = {}
for i in range(10):
    col = f'column_{i}'
    data[col] = range(5)
df_1 = pd.DataFrame(data)
# temp_col =

columns = st.multiselect("Columns:", df_1.columns)
filter = st.radio("Choose by:", ("show selected", "show unselected"))

if filter == "show unselected":
    columns = [col for col in df_1.columns if col not in columns]

if len(columns) != 0:
    df_1[columns]


company = st.multiselect("Company:", ['apple', 'google', 'nvidia', 'microsoft', 'coca-cola'], ['apple', 'google'])
chart_data = pd.DataFrame(
    np.random.randn(20, len(company)),
    columns=company)

st.line_chart(chart_data)


def initialize():
    if 'df' not in st.session_state:
        data = {}
        for i in range(5):
            col = f'column_{i}'
            data[col] = range(5)
        st.write('initializing')
        df = pd.DataFrame(data)
        st.session_state.df = df
        st.session_state.columns = list(df.columns)


initialize()

df = st.session_state.df
columns = st.session_state.columns


def move_column(col, state):
    if state:
        st.session_state[col] = True
        st.session_state.columns.remove(col)
    else:
        st.session_state[col] = False
        st.session_state.columns.append(col)


configure = st.columns(2)
with configure[0]:
    included = st.expander('Included', expanded=True)
    with included:
        st.write('')

with configure[1]:
    excluded = st.expander('Excluded', expanded=True)
    with excluded:
        st.write('')

for col in df.columns:
    if col in st.session_state.columns:
        with included:
            st.checkbox(col, key=col, value=False, on_change=move_column, args=(col, True))
    else:
        with excluded:
            st.checkbox(col, key=col, value=True, on_change=move_column, args=(col, False))

df[columns]

st.markdown('''<style>[data-testid="stExpander"] ul [data-testid="stVerticalBlock"] 
               {overflow-y:scroll; max-height:400px;} </style>''', unsafe_allow_html=True)


import streamlit as st
from os import listdir
from math import ceil
import pandas as pd
import re

uploaded_file = st.file_uploader("Choose a File", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
st.write(uploaded_file)
file_str_list = []
for i in range(0, len(uploaded_file)):
    rule = uploaded_file[i]
    st.write(rule)
    reg = re.compile(r'name=.*?\'(.*?)\', type')
    ruleMatch = reg.search(rule)
    if ruleMatch != None:
        file_list.append(ruleMatch.group(1))
        print(ruleMatch.group(1))

# directory = r'D:\\Streamlit\\test\\img'
# files = listdir(directory)
files = file_str_list
st.write(files)

def initialize():
    df = pd.DataFrame({'file':files,
                    'incorrect':[False]*len(files)})
    df.set_index('file', inplace=True)
    return df

if 'df' not in st.session_state:
    df = initialize()
    st.session_state.df = df
else:
    df = st.session_state.df


controls = st.columns(3)
with controls[0]:
    batch_size = st.select_slider("Batch size:", range(10,110,10))
with controls[1]:
    row_size = st.select_slider("Row size:", range(1,6), value = 5)
num_batches = ceil(len(files)/batch_size)
with controls[2]:
    page = st.selectbox("Page", range(1,num_batches+1))


def update(image, col):
    df.at[image,col] = st.session_state[f'{col}_{image}']
    if st.session_state[f'incorrect_{image}'] == False:
       df.at[image] = ''

batch = files[(page-1)*batch_size : page*batch_size]

grid = st.columns(row_size)
col = 0
for image in batch:
    with grid[col]:
        st.image(f'{directory}\{image}', caption=image)
        st.checkbox("Incorrect", key=f'incorrect_{str(image)}',
                    # value=df.at[image, 'incorrect'],
                    on_change=update, args=(image, 'incorrect'))
    col = (col + 1) % row_size

if 'incorrect' in df.columns:
    st.write('## Corrections needed')
    df[df['incorrect']==True]

