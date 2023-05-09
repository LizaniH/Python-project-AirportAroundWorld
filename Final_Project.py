"""
Name:       Lizzie Zhu
CS230:      Section 4
Data:       Airport all around world
URL:        Link to your web application on Streamlit Cloud (if posted)

Description:

This program includes:
Charts, data selection, sidebars, different pages, image using,
table, data analysis.
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


df = pd.read_csv("https://raw.githubusercontent.com/LizaniH/Python-project-AirportAroundWorld/main/airport.csv")
df['continent'].replace(np.nan, "NA", inplace=True)



def select_elevation(data,range_elevation):
    temp1 = data[int(range_elevation[-1]) >= data["elevation_ft"]]
    temp2 = temp1[int(range_elevation[0]) <= temp1["elevation_ft"]]
    return temp2

def get_xy_range(data):
    coordinates_x_dict = {}
    coordinates_y_dict = {}
    for i in range(len(data["coordinates"])):
        temp = data["coordinates"][i].split(", ")
        coordinates_x_dict[i] = float(temp[0])
        coordinates_y_dict[i] = float(temp[1])
    return coordinates_x_dict, coordinates_y_dict

def select_xy(data, range_x, range_y, coordinates_x_dict, coordinates_y_dict):
    drop = []
    x = coordinates_x_dict.copy()
    y = coordinates_y_dict.copy()
    for i in range(len(coordinates_x_dict)):
        if coordinates_x_dict[i] < range_x[0] or coordinates_x_dict[i] > range_x[1] or coordinates_y_dict[i] < range_y[0] or coordinates_y_dict[i] > range_y[1]:
            drop.append(i)
            del x[i]
            del y[i]            
    
    data = data.drop(drop)
    return data, list(x.values()), list(y.values())

def show_data(data, continent, set_index):
    D = data.set_index(set_index)
    D = D.loc[continent]
    return D


def pie_chart(bin_size,data,range_elevation):
    bins = range(range_elevation[0], range_elevation[-1], bin_size)  # start at 1915 and end at 2040 (not inclusive), with a step of bin_size years
    labels = [f"{b} - {b + bin_size - 1}" for b in bins[:-1]]  # create labels for each period
    data['elevation_ft_period'] = pd.cut(df['elevation_ft'], bins=bins, labels=labels, include_lowest=True)

    # count the number of stadiums built in each period
    counts = data['elevation_ft_period'].value_counts()

    # calculate the percentage of stadiums in each period
    percentages = counts / counts.sum() * 100
    
    show = {}
    not_show = {}
    
    for index in range(len(labels)):
        if percentages[index] < 1:
            not_show[labels[index]] = percentages[index]
        else:
            show[labels[index]] = percentages[index]
    
    return list(show.values()), list(show.keys())

def elevation_map(data,elevation_map_labels):
    fig, ax = plt.subplots()
    for i in elevation_map_labels:
        x = []
        y = []
        temp = select_elevation(data,i.split(" - "))
        for coor in temp["coordinates"]:
            temp_coor = coor.split(", ")
            x.append(float(temp_coor[0]))
            y.append(float(temp_coor[1]))
        ax.scatter(x, y, s = 1, label = i)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Locations of Airports')
    ax.legend()
    st.pyplot(fig)

img_ad = "https://images.pexels.com/photos/2026324/pexels-photo-2026324.jpeg?cs=srgb&dl=pexels-tanathip-rattanatum-2026324.jpg&fm=jpg"
def page_intro():
    st.title("Welcome to the Airports information")
    st.image(img_ad, caption= "..Airport under sunset..")
    st.write("This is the introduction page.")
    st.write("The program will help you to answer three questions:")
    st.write("1. A map that could adjusted its latitude and longitude.")
    st.write("2. The airport's details from your selections(elevation range, continent, country, types of airport)")
    st.write("3. A map and a pie chart that show all airports by its range of elevation. ")
    st.write("The Selected map and selected tables will answer question 1 and 2.")
    st.write("The Map and Chart will answer question 3.")
    if st.button("Selected map and selected tables"):
        page = "Selected map and selected tables"
        st.experimental_set_query_params(page=page)
        st.experimental_rerun()
        
    if st.button("Map and Chart"):
        page = "Map and Chart"
        st.experimental_set_query_params(page=page)
        st.experimental_rerun()
        
def page_1():
    st.title("Selected map and selected tables")
    st.write("the following will answer question 1 and 2. ")
    st.write("1. A map that could adjusted its latitude and longitude.")
    st.write("2. The airport's details from your selections(elevation range, continent, country, types of airport)")
    
    st.sidebar.header("SEARCH ANYTHING...")
    
    ### Get location of Airports
    coordinates_x_dict, coordinates_y_dict = get_xy_range(df)
    range_x = st.sidebar.slider("Please select your prefer Longitude (X coordiate):",
                                value=[int(min(list(coordinates_x_dict.values()))), int(max(list(coordinates_x_dict.values())))],
                                min_value=int(min(list(coordinates_x_dict.values()))),
                                max_value=int(max(list(coordinates_x_dict.values()))),
                                step=1)
    range_y = st.sidebar.slider("Please select your prefer Latitude (Y coordiate):",
                                value=[int(min(list(coordinates_y_dict.values()))), int(max(list(coordinates_y_dict.values())))],
                                min_value=int(min(list(coordinates_y_dict.values()))),
                                max_value=int(max(list(coordinates_y_dict.values()))),
                                step=1)
    df1, X, Y = select_xy(df, range_x, range_y, coordinates_x_dict, coordinates_y_dict)
    fig, ax = plt.subplots()
    ax.scatter(X, Y, s=1)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Locations of Airports')
    st.pyplot(fig)
    
    ### Select Airports by elevation
    range_elevation = st.sidebar.slider("Please select your prefer elevation:",
                                           value=[int(min(df["elevation_ft"])), int(max(df["elevation_ft"]))],
                                           min_value=int(min(df["elevation_ft"])),
                                           max_value=int(max(df["elevation_ft"])),
                                           step=1
                                           )
    df2 = select_elevation(df1, range_elevation)
    
    ### Select Airports by continent
    continent = st.sidebar.selectbox("Please select your continent:", set(df2["continent"]))
    df3 = show_data(df2, continent, "continent")
    
    countries = st.sidebar.multiselect("Please select your countries:", set(df3["iso_country"]))
    df4 = show_data(df3, countries, "iso_country")
    
    airport_type = st.sidebar.multiselect("Please select the type of your airport:", set(df4["type"]))
    df5 = show_data(df4, airport_type, "type")
    st.dataframe(df5)
    
    if st.button("Go back to Introduction"):
        page = "Intro"
        st.experimental_set_query_params(page=page)
        st.experimental_rerun()
        

def page_2():
    st.title("Map and Chart")
    st.write("This page will answer question 3:")
    st.write("3. A map and a pie chart that show all airports by its range of elevation. ")
    
    bin_size = 1000
    elevation_map_percentage, elevation_map_labels = pie_chart(bin_size,df,[-1266, 29977])
    
    # create a pie chart
    fig, ax = plt.subplots()
    ax.pie(elevation_map_percentage, labels = elevation_map_labels, autopct='%1.1f%%')
    
    ax.set_title("Percentage of Airports Built in {} Elevation Range".format(bin_size))
    st.pyplot(fig)
    st.write("The remaining portions of the airport, constructed during these elevation periods, constitute an exceedingly small fraction, hence their omission from the plot.")
    
    # create a map
    elevation_map(df,elevation_map_labels)
    
    if st.button("Go back to Introduction"):
        page = "Intro"
        st.experimental_set_query_params(page=page)
        st.experimental_rerun()
        
def main():
    page = st.experimental_get_query_params().get("page", ["Intro"])[0]
    
    if page == "Intro":
        page_intro()
    elif page == "Selected map and selected tables":
        page_1()
    elif page == "Map and Chart":
        page_2()

if __name__ == "__main__":
    main()
