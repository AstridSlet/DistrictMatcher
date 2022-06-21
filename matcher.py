from faulthandler import disable
import streamlit as st
import pandas as pd
import pydeck as pdk
import os
import geopandas as gpd
from urllib.error import URLError
import numpy as np


# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="CityExplorer")

# intitialise session state variables
if "w_security" not in st.session_state:
    st.session_state['w_security'] = 0

if "w_rent" not in st.session_state:
    st.session_state['w_rent'] = 0

if "w_nightlife" not in st.session_state:
    st.session_state['w_nightlife'] = 0 

if "w_culture" not in st.session_state:
    st.session_state['w_culture'] = 0

if "w_nature" not in st.session_state:
    st.session_state['w_nature'] = 0

if "w_shopping" not in st.session_state:
    st.session_state['w_shopping'] = 0


# functions for checking sum of sliders
def check_security():
    all_points = st.session_state.sho + st.session_state.cul + st.session_state.sec + st.session_state.ren + st.session_state.nat + st.session_state.nigh
    if all_points >100:
        st.warning('You can only distribute a maximum of 100 percent points. The other sliders were therefore reset.')
        st.session_state.cul = 0
        st.session_state.ren = 0
        st.session_state.nigh = 0
        st.session_state.nat = 0
        st.session_state.sho = 0        
    else:
        pass

def check_culture():
    all_points = st.session_state.sho + st.session_state.cul + st.session_state.sec + st.session_state.ren + st.session_state.nat + st.session_state.nigh
    if all_points >100:
        st.warning('You can only distribute a maximum of 100 percent points. The other sliders were therefore reset.')
        st.session_state.sec = 0
        st.session_state.ren = 0
        st.session_state.nigh = 0
        st.session_state.nat = 0
        st.session_state.sho = 0        
    else:
        pass

def check_nature():
    all_points = st.session_state.sho + st.session_state.cul + st.session_state.sec + st.session_state.ren + st.session_state.nat + st.session_state.nigh
    if all_points >100:
        st.warning('You can only distribute a maximum of 100 percent points. The other sliders were therefore reset.')
        st.session_state.sec = 0
        st.session_state.ren = 0
        st.session_state.nigh = 0
        st.session_state.cul = 0
        st.session_state.sho = 0        
    else:
        pass

def check_shopping():
    all_points = st.session_state.sho + st.session_state.cul + st.session_state.sec + st.session_state.ren + st.session_state.nat + st.session_state.nigh
    if all_points >100:
        st.warning('You can only distribute a maximum of 100 percent points. The other sliders were therefore reset.')
        st.session_state.sec = 0
        st.session_state.ren = 0
        st.session_state.nigh = 0
        st.session_state.nat = 0
        st.session_state.cul = 0        
    else:
        pass

def check_nightlife():
    all_points = st.session_state.sho + st.session_state.cul + st.session_state.sec + st.session_state.ren + st.session_state.nat + st.session_state.nigh
    if all_points >100:
        st.warning('You can only distribute a maximum of 100 percent points. The other sliders were therefore reset.')
        st.session_state.sec = 0
        st.session_state.ren = 0
        st.session_state.cul = 0
        st.session_state.nat = 0
        st.session_state.sho = 0        
    else:
        pass

def check_rent():
    all_points = st.session_state.sho + st.session_state.cul + st.session_state.sec + st.session_state.ren + st.session_state.nat + st.session_state.nigh
    if all_points >100:
        st.warning('You can only distribute a maximum of 100 percent points. The other sliders were therefore reset.')
        st.session_state.sec = 0
        st.session_state.cul = 0
        st.session_state.nigh = 0
        st.session_state.nat = 0
        st.session_state.sho = 0        
    else:
        pass

# create reset function for reset button
def reset_func():
    st.session_state.sec = 0
    st.session_state.cul = 0
    st.session_state.nigh = 0
    st.session_state.nat = 0
    st.session_state.sho = 0
    st.session_state.ren = 0

#@st.cache    
# Load spatial data
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

 

# load dummy data
df = pd.read_excel(os.path.join("data", "dummy_data.xlsx"))

# add coordinates
df['coordinates'] = all_coords

# create dummy variable for attractiveness
df["attractiveness"] = np.random.random(10) # assign random float between 0 and 1 to test coloring
df["attractiveness"] = df["attractiveness"].round(2)

col1_0, col2_0 = st.columns([9,1])
with col1_0:
    st.title("Moving to Copenhagen?")
    st.subheader("Find the district that suit your needs.")
with col2_0:
    st.image(os.path.join('img','logo.png'), width=100)



# TOP SECTION
col1_1, col2_1, col3_1 = st.columns(3)

# define options for selectsliders
opts = range(0,110, 10)

with col1_1:
    st.write(" ")
    st.write(" ")
    st.write("Whether you are looking to move to Copenhagen for the first time, or have a wish to find a new area to live in, this tool can help guide your search for a new home.")
    st.write("Use the sliders to indicate how important each of the parameters are to you.")
    st.write("You can distribute **100 percent points** between the six variables that are displayed.")
    st.write("The map below will then display which areas best matches your preferences.")


# explanatory texts 
security_help = 'Based on number of crimes per inhabitant in the area.'
rent_help = 'Based on average cost per square meter in rented apartments of the area.'
nightlife_help = 'Based on number of bars and restaurants in the area.'
with col2_1: 
    st.markdown("---")   
    w_security= st.select_slider(label = 'Security',
        options=opts, value = 0, key = 'sec', help=security_help, on_change = check_security)

    w_rent = st.select_slider( label ='Low rent',
        options=opts, value = 0, key = 'ren', help=rent_help, on_change = check_rent)

    w_nightlife = st.select_slider( label = 'Bars/restaurants',
        options=opts, value = 0, key = 'nigh', help=nightlife_help, on_change = check_nightlife)

# explanatory texts 
culture_help = 'Based on number of theaters, cinemas and museums in the area.'
nature_help = 'Based on number of parks and green areas in the area.'
shopping_help = 'Based on number of supermarkets and retailstores in the area.'

with col3_1:  
    st.markdown("---") 
    w_culture = st.select_slider(label = 'Culture',
        options=opts, value = 0, key = 'cul', help=culture_help, on_change = check_culture)

    w_nature = st.select_slider( label = 'Nature',
        options=opts, value = 0, key = 'nat', help=nature_help, on_change = check_nature)

    w_shopping = st.select_slider( label = 'Shopping',
        options=opts, value = 0, key = 'sho', help=shopping_help, on_change = check_shopping)

########## Inform user about how many points they have used ########
col_a, col_b = st.columns([1, 0.15])
with col_a:
    distributed_points = st.session_state.sho + st.session_state.cul + st.session_state.sec + st.session_state.ren + st.session_state.nat + st.session_state.nigh

    st.write(f"**Distributed points: {distributed_points}**")
    if distributed_points < 100:
        st.write(f"**You still need to distribute {100-distributed_points} points!**")
    elif distributed_points == 100:
        st.write(f"**You have distributed the correct amount of points.**")
        st.write(f"**Go explore the map below!**")
    else:
        pass

with col_b:
    st.markdown(" ")
    st.markdown(" ")
    reset_button = st.button('Reset sliders', on_click = reset_func)


### UPDATING MATCH SCORES IN THE MAP #####
# gather the weights in list
weights = [st.session_state.sec, st.session_state.ren, st.session_state.nigh, st.session_state.cul, st.session_state.nat, st.session_state.sho]

# update match scores
def get_score(data, weight_list):
    """
    Function that takes in a dataframe and a list of weights
    Multiply values in collumns with the corresponding weights
    Sum the values to get a total attractiveness score for each neighborhood
    """
    col_list = ['security', 'rent', 'nightlife', 'culture', 'nature', 'shopping']
    for col, weight in zip(col_list, weight_list):
        data[col] = data[col] * weight
    
    # calculate attractiveness
    data['attractiveness'] = ((data[col_list].sum(axis=1))/100)
    return data


# update attractiveness scores for the ten districts using the weights list
df = get_score(df, weights)

# get top 3 match 
top_match_idx = df['attractiveness'].nlargest(3).index.tolist()

top_match1 = df.iloc[top_match_idx[0], 0]
top_match2 = df.iloc[top_match_idx[1], 0]
top_match3 = df.iloc[top_match_idx[2], 0]



########## Defining stuff for the map ########

# Custom color scale with 5 colors 
COLOR_RANGE = [
    [241,238,246],
    [189,201,225],
    [116,169,207],
    [43,140,190],
    [4,90,141]]

# The five height levels
HEIGHT_RANGE = [
    0,
    500,
    1000,
    1500,
    2000] 
    
# assigning cutoff value for each color/height level 
BREAKS = [0.2, 0.4, 0.6, 0.8, 1]

def color_scale(val):
    """
    Takes in a match value between 0 and 1
    Returns one of 5 RGB color codes according to the value   
    """
    for i, b in enumerate(BREAKS):
        if val < b:
            return COLOR_RANGE[i]
    return COLOR_RANGE[i]


def get_height(val):
    """
    Takes in a match value between 0 and 1
    Returns height value (one of the five possible heights) according to cutoff values  
    """
    for i, b in enumerate(BREAKS):
        if val < b:
            return HEIGHT_RANGE[i]
    return HEIGHT_RANGE[i]


# use height and color function to assign values based on attractiveness calculation
df["fill_color"] = df["attractiveness"].apply(color_scale) # color on the map by the libraries variable
df["elevation"] = df["attractiveness"].apply(get_height) # create elevation on the map from the attractiveness variable 


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

tooltip = {"html": "<strong> Area: {district} </strong> <br> <strong> Match: {attractiveness} </strong> <br> ----------------- <br> Security: {security_orig} <br> Rent: 0.8 <br> Bars/restaurants: {nightlife_orig} <br> Culture: {culture_orig} <br> Nature: {nature_orig} <br> Shopping: {shopping_orig} "}



######## Plotting the map section in streamlit ########
col1_2, col2_2,col2_3 = st.columns([1, 2, 0.4])

with col1_2:
    st.markdown("---")
    st.markdown('##### Your top 3 areas:')
    st.write(f"1. {top_match1}")
    st.write(f"2. {top_match2}")
    st.write(f"3. {top_match3}")
    
    #st.write('If you want to learn more about the area, you can read more **here**.')

    

with col2_2:
    st.markdown("---")
    st.write("**Explore the map to learn more about the different districts!**")
    # Plotting the map 
    st.pydeck_chart(pdk.Deck(
        polygon_layer,
        initial_view_state=view_state,
        map_style=pdk.map_styles.LIGHT,
        tooltip=tooltip))
    

with col2_3:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write("**Match scores**")
    st.image(os.path.join('img','legend.png'), width=100)


def plus_one():
    if st.session_state["slider"] < 10:
        st.session_state.slider += 1
    else:
        pass
    return

