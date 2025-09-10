# Import python packages
import streamlit as st
import requests
import pandas
from snowflake.snowpark.functions import col
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custome Smoothie!
  """
)



name_on_order = st.text_input("Name on Smoothie", "My name is...")
st.write("The name on your Smoothie will be:", name_on_order)
# orders_filled = False
# Get the current credentials

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Bananas", "Strawberries", "Peaches"),
# )

# st.write("Your favorite fruit is:", option)

# # session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, width='stretch')

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
    # default=["Yellow", "Red"],
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

      
        st.subheader(fruit_chosen + ' Nutrition Information')
        # st.write(search_on)
        st.write(fruit_chosen)
        fruityvice_response = requests.get('https://fruityvice.com/apu/fruit/' + search_on)
        st.write(fruityvice_response)
        st.stop()
        fv_df = st.dataframe(data=fruityvice_response.json(), width='stretch')

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

