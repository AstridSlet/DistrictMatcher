import streamlit as st
import pandas as pd
import pydeck as pdk
import os
import geopandas as gpd
from urllib.error import URLError
import numpy as np


# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="CityExplorer")

#@st.cache    
# Load data
districts_orig = gpd.read_file(os.path.join("data", "districts.json"))
districts = districts_orig.explode(index_parts=True) # flatten multipolygon into one polygon per district

all_coords = []
for i in range(10):
    if i != 3: # this exception is for handling the polygon of Indre By correctly
        polygon = districts.geometry[i][0] # extract one polygon (district) at a time
    if i == 3:
        polygon = districts.geometry[i][1]
    coords_list = [[[x,y] for (x,y) in polygon.exterior.coords]] # extract exterior coordinates of that area
    all_coords.append(list(coords_list)) # save cordinates in list of x,y coordinates
 
df = pd.DataFrame() # save coordinates in a df 
df["area"] = districts_orig['navn']
df["attractiveness"] = np.random.random(10) # assign random float between 0 and 1 to test coloring
df["attractiveness"] = df["attractiveness"].round(2)
df['coordinates'] = all_coords






# Custom color scale with 5 colors 
COLOR_RANGE = [
    [241,238,246],
    [189,201,225],
    [116,169,207],
    [43,140,190],
    [4,90,141]
]
    
    

# assigning cutoff value for each color level 
BREAKS = [0.0, 0.2, 0.4, 0.6, 0.8]

def color_scale(val):
    """
    Takes in a color value between 0 and 1
    Returns one of 5 RGB color codes according to the value   
    """
    for i, b in enumerate(BREAKS):
        if val < b:
            return COLOR_RANGE[i]
    return COLOR_RANGE[i]


def calculate_elevation(val):
    return val * 1000

df["fill_color"] = df["attractiveness"].apply(color_scale) # color on the map by the libraries variable
df["elevation"] = df["attractiveness"].apply(calculate_elevation) # create elevation on the map from the attractiveness variable 

view_state = pdk.ViewState(   
  latitude=55.656098,
  longitude=12.568337,
  zoom=11.2,
  max_zoom=16,
  pitch=45,
  bearing=0
)

polygon_layer = pdk.Layer(
    "PolygonLayer",
    df,
    id="geojson",
    opacity=0.9,
    stroked=False,
    get_polygon="coordinates",
    filled=True,
    extruded=True, # whether to elevate the leval of the polygons from the rest of the map
    wireframe=True, # whether to display/show the boundaries between the polygons or not (as lines)
    get_elevation="elevation",
    get_fill_color="fill_color",
    get_line_color=[43, 97, 136],
    auto_highlight=True,
    pickable=True,
)

tooltip = {"html": "<strong> Area: {area} </strong> <br> <strong> Match: {attractiveness} </strong> <br> ----------- <br> Security: 0.9 <br> Rent: 0.8 <br> Bars/restaurants: 0.2 <br> Culture: 0.1 <br> Nature: 0.5 <br> Shopping: 0.7 "}

col1_0, col2_0 = st.columns([9,1])
with col1_0:
    st.title("Moving to Copenhagen?")
    st.subheader("Find the borough that matches your needs.")
with col2_0:
    st.image(os.path.join('img','logo.png'), width=100)



# TOP SECTION
col1_1, col2_1, col3_1 = st.columns(3)

# define options
opts = range(0,110, 10)

with col1_1:
    st.write(" ")
    st.write(" ")
    st.write("Whether you are looking to move to Copenhagen for the first time, or have a wish to find a new area to live in, this tool can help guide your search for a new home.")
    st.write("Use the sliders to indicate how important each of the parameters are to you.")
    st.write("You can distribute 100 points between the six variables that are displayed.")
    st.write("The map below will then display which areas best matches your preferences.")

# explanatory texts 
security_help = 'This variable coverst the number of crimes per inhabitatnt in the area.'
rent_help = 'This variable covers the average cost per square meter in rented apartments of the area.'
nightlife_help = 'This variable covers the number of bars and restaurants in the area.'
with col2_1: 
    st.markdown("---")   
    security = st.select_slider(
        'Security',
        options=opts, help=security_help)

    rent = st.select_slider(
        'Rent',
        options=opts, help=rent_help)

    nightlife = st.select_slider(
        'Bars/restaurants',
        options=opts, help=nightlife_help)

# explanatory texts 
culture_help = 'This variable covers the number of theaters, cinemas and museums in the area.'
nature_help = 'The variable covers the number of parks and green areas in the area.'
shopping_help = 'This variable covers a count of the number of supermarkets and retailstores in the area.'

with col3_1:  
    st.markdown("---") 
    culture = st.select_slider("Culture",
        options=opts, help=culture_help)

    nature = st.select_slider(
        'Nature',
        options=opts, help=nature_help)

    sport = st.select_slider(
        'Shopping',
        options=opts, help=shopping_help)


# MAP SECTION
col1_2, col2_2,col2_3 = st.columns([1, 2, 0.2])

with col1_2:
    st.markdown("---")
    st.markdown('##### The area that best matches your wishes is:')
    st.markdown('#### Østerbro')
    #top_match = '<p style="font-family:serif; color:Blue; font-size: 30px;">Østerbro</p>'
    #st.markdown(top_match, unsafe_allow_html=True)
    
    st.write('If you want to learn more about the area, you can read more **here**.')
    

with col2_2:
    st.markdown("---")
# Plotting the map 
    st.pydeck_chart(pdk.Deck(
        polygon_layer,
        initial_view_state=view_state,
        map_style=pdk.map_styles.LIGHT,
        tooltip=tooltip))
    st.write("Explore the map and discover how well the boroughs match your preferences!")

with col2_3:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.image(os.path.join('img','legend.png'), width=100)

# Adding additional info about the best matching borough
#col1_3, col2_3 = st.columns(2)

#with col1_3:
    #st.write("Key variables")




