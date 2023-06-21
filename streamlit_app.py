import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')

streamlit.header(' Breakfast Favorites')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


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

#create the repeatable code block - during the website loading phase this part of the code is skipped until its called
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice) 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#NEW SECTION to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')#kiwi is the default fruit
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function =  get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
    
except URLError as e:
    streamlit.error()


#### THIS CODE BELOW HAS BEEN MOVED TO THE TRY CATCH THERE IS JUST SOME OTHER STUFF AS WELL
#streamlit.text(fruityvice_response.json()) #just writes the data to the screen

#takes the json format of the response and normalizes it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#want to see how thte normalized way would be in a text file
#streamlit.text(fruityvice_normalized) - just like a table but without the lines

#put it into a proper dataframe through streamlit
#streamlit.dataframe(fruityvice_normalized)



streamlit.header('The fruit load list contains:')
#Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
    
# add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close() #closing snowflake connection for this function
    streamlit.dataframe(my_data_rows)


# don't run anything past here while we troubleshoot
# streamlit.stop()


## allow the end user to add a fruit to the lsit
def insert_row_snowflake (new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
        return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)
streamlit.write('Thanks for adding', add_my_fruit)


