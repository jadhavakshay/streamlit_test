import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from io import StringIO

st.title("Streamlit")

from sqlalchemy import create_engine
if st.button('Connect to master table'):
    conn = create_engine("mysql://admin:-S1rHz(A(Yz9$cWQqwvhB]d-+LC5@ratingsai-dev-mysql-standalone.csfbi9h6dndo.us-east-1.rds.amazonaws.com/ai_spherexratings?charset=utf8mb4")
    SQL_Query = pd.read_sql('SELECT Flag, RollUpStatus, CreatedDate, ExecutionFolderId, TitleId, TotalRuntime, SeriesOrFeatureName, ImageStatus, SceneStatus, TextStatus, AudioStatus, PaymentFlag FROM ai_spherexratings.mastertable where PaymentFlag=1 and CreatedDate >= DATE_ADD(CURDATE(), INTERVAL -5 DAY) order by CreatedDate desc;', conn)
    st.write("### AI Data Verification")
    df = pd.DataFrame(SQL_Query, columns=['Flag', 'RollUpStatus', 'CreatedDate', 'ExecutionFolderId', 'TitleId',
                                                'TotalRuntime', 'SeriesOrFeatureName', 'ImageStatus', 'SceneStatus',
                                                'TextStatus', 'AudioStatus', 'PaymentFlag'])
    st.dataframe(data=df)

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
    if 'df_2' not in st.session_state:
        data = {}
        for i in range(5):
            col = f'column_{i}'
            data[col] = range(5)
        st.write('initializing')
        df_2 = pd.DataFrame(data)
        st.session_state.df_2 = df_2
        st.session_state.columns = list(df_2.columns)


initialize()

df_2 = st.session_state.df_2
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

for col in df_2.columns:
    if col in st.session_state.columns:
        with included:
            st.checkbox(col, key=col, value=False, on_change=move_column, args=(col, True))
    else:
        with excluded:
            st.checkbox(col, key=col, value=True, on_change=move_column, args=(col, False))

df_2[columns]

st.markdown('''<style>[data-testid="stExpander"] ul [data-testid="stVerticalBlock"] 
               {overflow-y:scroll; max-height:400px;} </style>''', unsafe_allow_html=True)


import streamlit as st
from os import listdir
from math import ceil
import pandas as pd
import re

uploaded_files = st.file_uploader("Choose a File", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
file_str_list = []
for uploaded_file in uploaded_files:
    file_str_list.append(uploaded_file.name)

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
        st.write(df)
        df.loc[df.file == image, 'incorrect'] = ''
        # df.at[image] = ''

# st.write(type(files))
# st.write('files --------------', files)
img_icon_list = []
if len(files) > 0:
    batch = files[(page-1)*batch_size : page*batch_size]
    grid = st.columns(row_size)
    col = 0
    for uploaded_file in uploaded_files:
        for image in batch:
            with grid[col]:
                if uploaded_file.name == image:
                    show_img = uploaded_file.read()
                    img_icon_list.append(show_img)
                    st.image(show_img, caption=image)
                    st.checkbox("Incorrect", key=f'incorrect_{str(image)}',
                                # value=df.at[image, 'incorrect'],
                                on_change=update, args=(str(image), 'incorrect'))
            col = (col + 1) % row_size
    
    if 'incorrect' in df.columns and len(df[df['incorrect'] == True]) > 0:
        st.write('## Corrections needed')
        df[df['incorrect']==True]

df_new = pd.DataFrame(
    [
        [2768571, 130655, 1155027, 34713051, 331002277],
        [1448753, 60632, 790040, 3070447, 212558178],
        [654405, 9536, 422931, 19852167, 145934619],
        [605216, 17848, 359891, 8826585, 1379974505],
        [288477, 9860, 178245, 1699369, 32969875],
    ],
    columns=[
        "Total Cases",
        "Total Deaths",
        "Total Recovered",
        "Total Tests",
        "Population",
    ],
)
df_new["Country"] = img_icon_list[0:5]
def path_to_image_html(path):
    return '<img src="' + path + '" width="60" >'


st.markdown(
    df_new.to_html(escape=False, formatters=dict(Country=path_to_image_html)),
    unsafe_allow_html=True,
)

# Saving the dataframe as a webpage - works
if st.button('Download data as HTML'):
    df_new.to_html("webpage.html", escape=False, formatters=dict(Country=path_to_image_html))
