from django.shortcuts import render

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx

import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
 
# Create your views here.
def home_page_main(request):

    # Reading the Inputs
    # file_path = r"E:\Work\UpWork Projects\Olawale Lawal Lawal - Interactive Map\Data\landmarks-and-places-of-interest-including-schools-theatres-health-services-spor.csv"
    file_path = str(BASE_DIR) + r"\templates\Data\landmarks-and-places-of-interest-including-schools-theatres-health-services-spor.csv"

    landmarks_df = pd.read_csv(file_path)

    # Getting Unique Themes
    themes = landmarks_df["theme"].values.tolist()
    unique_themes = np.unique(themes).tolist()

    themes_and_subthemes_dict = {key: [] for key in themes}    

    for idx in landmarks_df.index:
        theme = landmarks_df.iloc[[idx]]["theme"].values.tolist()[0].strip()
        sub_theme = landmarks_df.iloc[[idx]]["sub_theme"].values.tolist()[0].strip()
        themes_and_subthemes_dict[theme].append(sub_theme)

    for key in themes_and_subthemes_dict:
        themes_and_subthemes_dict[key] = np.unique(themes_and_subthemes_dict[key]).tolist()


    if request.method == "POST":
        
        chosen_theme = request.POST.get("unique_theme")
        chosen_sub_theme = request.POST.get("unique_sub_theme")

        chosen_df = landmarks_df.loc[landmarks_df['theme'] == chosen_theme]
        chosen_df = chosen_df.loc[chosen_df['sub_theme'] == chosen_sub_theme]

        fig = px.scatter_mapbox(chosen_df,
                                lon=chosen_df["lon"], 
                                lat=chosen_df["lat"], 
                                zoom=10, 
                                color=chosen_df["mark_on_map_color"], 
                                size=chosen_df["mark_on_map_size"], 
                                width=1200,
                                height=900, 
                                title="Car Share Scatter",
                                hover_data={
                                "feature_name": True,
                                "mark_on_map_color": False,
                                "mark_on_map_size": False}
                                )
    
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})
        fig.show()

    context = {"unique_themes": unique_themes, "themes_and_subthemes_dict": themes_and_subthemes_dict}

    return render(request, "homepage/home.html", context)


def cafes_view_main(request):

    cafes_file_path = str(BASE_DIR) + r"\templates\Data\cafes-and-restaurants-with-seating-capacity.xlsx"
    print("Reading Cafes")
    cafes_df = pd.read_excel(cafes_file_path)
    print("DONE")

    cafes_categories = cafes_df["industry_anzsic4_description"].values.tolist()
    cafes_categories = np.unique(cafes_categories).tolist()

    if request.method == "POST":
        
        chosen_category = request.POST.get("Category")

        chosen_df = cafes_df.loc[cafes_df['industry_anzsic4_description'] == chosen_category]

        print(chosen_df)

        fig = px.scatter_mapbox(chosen_df,
                                lon=chosen_df["longitude"], 
                                lat=chosen_df["latitude"], 
                                zoom=10, 
                                color=chosen_df["block_id"], 
                                size=chosen_df["property_id"], 
                                width=1200,
                                height=900,
                                hover_data={
                                "industry_anzsic4_description": True,
                                "business_address": True,
                                "trading_name": True}
                                )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})
        fig.show()

    context = {"cafes_categories": cafes_categories}
    
    return render(request, "homepage/cafes.html", context)