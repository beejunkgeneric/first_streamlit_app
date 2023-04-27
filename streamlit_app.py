
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header ('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
#Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#streamlit.dataframe(my_fruit_list)

#Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

#display the table on the page
#streamlit.dataframe(my_fruit_list)

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
 # fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
 else:
   back_from_function = get_fruityvice_data(fruit_choice)
   streamlit.dataframe(back_from_function)
      #fruitvice_response = requests.get("https://fruitvice.com/api/fruit/" + fruit_choice)
      #fruitvice_normalized = pandas.json_normalize(fruityvice_response.json())
      #streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()
  
streamlit.write('The user entered', fruit_choice)

#import requests

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#streamlit.text(fruityvice_response.json())

# this pulls the fruits into a variable
#take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# this adds the border for fruit display?
#output it the screen as a table
streamlit.dataframe(fruityvice_normalized)

streamlit.header("The fruit load list contains:")
#import snowflake.connector
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
       my_cur.execute("select * from fruit_load_list")
       return my_cur.fetchall()
      
#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'): 
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
#my_data_rows = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
#my_data_row = my_cur.fetchone()
#streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
       my_cur.execute("insert into fruit_load_list values ('from streamlit')")
       return "Thanks for adding " + new_fruit
      
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        back_from_function = insert_row_snowflake(add_my_fruit)
        streamlit.text(back_from_funtion)
        

#streamlit.write('Thanks for adding', add_my_fruit)

#This will not work correctly, but just go with it for now
#my_cur.execute("insert into fruit_load_list values('from streamlit')")


