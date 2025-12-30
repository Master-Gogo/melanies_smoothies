# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custome Smoothie!
  """
)


# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("Your favorite fruit is:", option)
name_on_order=st.text_input("Name on Smoothie:")
st.write("the name on your Smoothie wiil be:",name_on_order)
#from snowflake.snowpark.functions import col
#session = get_active_session()
cnx=st.connection('snowflake')
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("SEARCH_ON"))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
ingradient_list=st.multiselect("choose upto 5 ingradient :", my_dataframe,max_selections=5)
if ingradient_list:
    # st.write(ingradient_list)
    # st.text(ingradient_list)
    ingradient_string=''
    for fruit_choosen in ingradient_list:
        ingradient_string=ingradient_string+fruit_choosen+' '
        st.subheader(fruit_choosen + 'Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_choosen)
        sf_df=st.dataframe(smoothiefroot_response.json(), use_container_width=True)
    #st.write(ingradient_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingradient_string + """','""" + name_on_order + """')"""
    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button(" submit order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


    
