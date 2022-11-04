import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn')

st.title('CO2_Emissions and Fuel Consumption by Cars')
df = pd.read_csv('Sample.csv')
df = df.loc[:, ['MODEL', 'MAKE', 'MODEL.1', 'VEHICLE CLASS', 'ENGINE_SIZE', 'CYLINDERS','TRANSMISSION', 'FUEL', 'FUEL_CONSUMPTION*', 'CO2_EMISSIONS']]


fuel_consumption_filter = st.slider('fuel consumption:', 4, 24, 6)  # min, max, default

# create a multi select
vehicle_class_filter = st.sidebar.multiselect(
     'Choose the vehicle class',
     df['VEHICLE CLASS'].unique(),  # options
     df['VEHICLE CLASS'].unique(),)  # defaults

genre = st.sidebar.radio(
    "Choose CO2 Emissions level",
    ('No Choose','Low', 'Medium', 'High'))

if genre == 'Low':
    df = df[df.CO2_EMISSIONS <= 200]
elif genre == 'Medium':
    df = df[(df.CO2_EMISSIONS > 200) & (df.CO2_EMISSIONS < 400)]
elif genre == 'High':
    df = df[df.CO2_EMISSIONS >= 400]

# create a input form
form = st.sidebar.form("brand_form")
brand_filter = form.text_input('Car Brand (enter ALL to reset)', 'ALL')
form.form_submit_button("Apply")
    
if brand_filter!='ALL':
    df = df[df.MAKE == brand_filter]
    


# filter by fuel_consumption
df = df[df['FUEL_CONSUMPTION*'] >= fuel_consumption_filter]

# filter by vehicle class
df = df[df['VEHICLE CLASS'].isin(vehicle_class_filter)]





# show the plot
st.subheader('fuel consumption by different brand of cars')
fig, ax = plt.subplots( figsize=(10,5))

df.groupby('MAKE')['FUEL_CONSUMPTION*'].mean().sort_values().plot.bar(ax=ax)
plt.xticks(rotation=70)
st.pyplot(fig)


st.subheader('fuel consumptions')
fig, ax = plt.subplots(figsize=(20, 10))
df['FUEL_CONSUMPTION*'].hist(bins=50)
st.pyplot(fig)


# show dataframe
st.subheader('Emissions by different model:')
st.write(df[['MAKE', 'MODEL.1', 'CO2_EMISSIONS']].sort_values('CO2_EMISSIONS'))
st.subheader('Fuel Consumption by different model:')
st.write(df[['MAKE', 'MODEL.1', 'FUEL_CONSUMPTION*']].sort_values('FUEL_CONSUMPTION*'))


# CO2 EMISSIONS and Fuel consumption by different cylinders
st.subheader('CO2 emissions and Fuel consumption by different cylinders')

# show line chart
fig, ax = plt.subplots(1, 2, figsize=(10,5))
df.groupby('CYLINDERS')['CO2_EMISSIONS'].mean().plot(ax=ax[0], linestyle='dotted', color='red', marker='o')
df.groupby('CYLINDERS')['FUEL_CONSUMPTION*'].mean().plot(ax=ax[1], linestyle='dashed', color='green', marker='*')
ax[0].set_title('CO2_EMISSIONS')
ax[1].set_title('Fuel_consumption')
st.pyplot(fig)

# show pie chart
fig, ax = plt.subplots(1, 2, figsize=(10,5))
df.groupby('CYLINDERS')['CO2_EMISSIONS'].mean().plot.pie(ax=ax[0], autopct='%1.1f%%')
df.groupby('CYLINDERS')['FUEL_CONSUMPTION*'].mean().plot.pie(ax=ax[1], autopct='%1.1f%%')
st.pyplot(fig)

