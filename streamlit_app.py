import streamlit


streamlit.title('My Parents New Healthy Diner')

streamlit.header(' Breakfast Favorites')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include - lesson 3 early part of the lesson
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

#this way we will be able to pre populate 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected] #pandas.datraframe.loc[]

#display table on the page -- earlier step displaying all the fruits
#streamlit.dataframe(my_fruit_list)


#display the table on the page - only selected fruits
streamlit.dataframe(fruits_to_show)


#NEW SECTION to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')#kiwi is the default fruit
streamlit.write('the user entered', fruit_choice)


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json()) #just writes the data to the screen

#takes the json format of the response and normalizes it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#want to see how thte normalized way would be in a text file
#streamlit.text(fruityvice_normalized) - just like a table but without the lines

#put it into a proper dataframe through streamlit
streamlit.dataframe(fruityvice_normalized)
