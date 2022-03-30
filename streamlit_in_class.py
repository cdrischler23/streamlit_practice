import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

##### Title and intro

st.title( 'Mortgage Data Streamlit App' )
st.write()


data = pd.read_csv('practice-project-dataset-1.csv')
data.head()

sex_list = []
for sex in data['derived_sex']:
    if sex not in sex_list:
        sex_list.append(sex)

race_list = []
for race in data['derived_race']:
    if race not in race_list:
        race_list.append(race)

##### Inputs

st.header('Please choose from the two dropdowns')

selected_sex = st.selectbox('Please choose a sex from the dropdown',sex_list)
selected_race = st.selectbox('Please choose a race from the dropdown',race_list)

st.write('You selected:' , selected_sex, ',', selected_race)

filtered_data1 = data.loc[data['derived_sex'] == selected_sex]
graph_data = filtered_data1.loc[filtered_data1['derived_race'] == selected_race]

graph_data['approved'] = np.where(graph_data['action_taken'] < 3, 1, 0)

graph_data['property_value'] = graph_data['property_value'].replace('Exempt', np.nan).astype(float)

final = graph_data.groupby('state_code')[['property_value', 'approved']].agg({'property_value': 'median', 'approved': 'mean'})

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

plt.scatter(final['property_value'], final['approved'])
plt.xlabel('Median Property Value')
plt.ylabel('Fraction of Applicants Approved')

st.write(fig)