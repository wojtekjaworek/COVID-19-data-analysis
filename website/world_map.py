import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy as sc
import pandas as pd
import folium
from flask import Flask, render_template, Blueprint
import cartopy as cp
import requests
import json


def fields_for_geoJSON_tooltips(country, data):

    data = data[data['Name'] == country]
    size = np.shape(data)[1]
    data = data.values.tolist()

    try:
        data = data[0] # drop nested list into 1-D standard list

    except:
        None
    if len(data) == 0:
        print(f'no data for {country}')
        for i in range(size):
            data.append('no data')
    return data


def aliases_for_geoJSON_tooltips(country, data):
    data = data[data['Name'] == country]
    data = data.columns.values.tolist()
    return data


def extend_geoJSON(data, countries):

    # TODO: replace default values to something meaningful, maybe like 'no data', instead of presenting data for Poland

    default_keys = aliases_for_geoJSON_tooltips('Poland', data)
    detaulf_values = fields_for_geoJSON_tooltips('Poland', data)
    default_temp = zip(default_keys, detaulf_values)
    default_temp = list(default_temp)

    for country in countries['features']:
        keys = aliases_for_geoJSON_tooltips(country['properties']['name'], data)
        values = fields_for_geoJSON_tooltips(country['properties']['name'], data)


        temp = zip(keys, values)

        temp = list(temp)

        # Loop over GeoJSON features and add the new properties

        if country['properties']['name']:
            for i in range(len(temp)):
                country['properties'][temp[i][0]] = temp[i][1]

    return countries



def rename_countries(countries, list_of_countries_to_replace, list_of_countries_to_be_replaced):
    i = 0
    for country in countries['features']:
        if country['properties']['name'] == list_of_countries_to_be_replaced[i]:
            country['properties']['name'] = list_of_countries_to_replace[i]
            i += 1
            if i == len(list_of_countries_to_replace):
                break
    return countries

def world_map_options_list():
    list = [
        'Cases - cumulative total',
        'Cases - cumulative total per 100000 population',
        'Cases - newly reported in last 7 days',
        'Cases - newly reported in last 7 days per 100000 population',
        'Cases - newly reported in last 24 hours',
        'Deaths - cumulative total',
        'Deaths - cumulative total per 100000 population',
        'Deaths - newly reported in last 7 days',
        'Deaths - newly reported in last 7 days per 100000 population',
        'Deaths - newly reported in last 24 hours']
    return list


def create_world_map(option='Cases - cumulative total'):
    # WHO official tracked data about new cases worldwide
    # CASES_DATA_URL = 'https://covid19.who.int/WHO-COVID-19-global-table-data.csv'
    CASES_DATA_URL = 'covid19.who.int/WHO-COVID-19-global-table-data (5).csv'
    VACCINATION_DATA_URL = 'https://covid19.who.int/who-data/vaccination-data.csv'

    # headers:
    # Name, WHO Region,
    # Cases - cumulative total,
    # Cases - cumulative total per 100000 population,
    # Cases - newly reported in last 7 days,
    # Cases - newly reported in last 7 days per 100000 population,
    # Cases - newly reported in last 24 hours,
    # Deaths - cumulative total,
    # Deaths - cumulative total per 100000 population,
    # Deaths - newly reported in last 7 days,
    # Deaths - newly reported in last 7 days per 100000 population,
    # Deaths - newly reported in last 24 hours,
    # Transmission Classification
    cases = pd.read_csv(CASES_DATA_URL, delimiter=',', quotechar='"', encoding="utf8", header=0)



    # drop rows
    to_drop = ['Global']
    for d in to_drop:
        cases = cases[cases.Name != d]






    countries_list_to_compare = []
    countries_list_to_compare.extend(cases["Name"])  # list of countries names


    map = folium.Map()

    geoJSON_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    country_shapes = f'{geoJSON_url}/world-countries.json'

    countries = requests.get(country_shapes).json()


    list_of_countries_from_data = ['Bahamas',
                         'Bolivia (Plurinational State of)',
                         'Brunei Darussalam',
                         'Côte d’Ivoire',
                         'Congo',
                         'Czechia',
                         'Falkland Islands (Malvinas)',
                         'The United Kingdom',
                         'Guinea-Bissau',
                         'Iran (Islamic Republic of)',
                         'Republic of Korea',
                         'Kosovo[1]',
                         "Lao People's Democratic Republic",
                         'Republic of Moldova',
                         'North Macedonia',
                         "Democratic People's Republic of Korea",
                         'Russian Federation',
                         'Serbia',
                         'Eswatini',
                         'Syrian Arab Republic',
                         'Timor-Leste',
                         'Venezuela (Bolivarian Republic of)',
                         'Viet Nam',
                         'occupied Palestinian territory, including east Jerusalem']

    list_of_countries_from_geoJSON = ['The Bahamas',
                                      'Bolivia',
                                      'Brunei',
                                      'Ivory Coast',
                                      'Republic of the Congo',
                                      'Czech Republic',
                                      'Falkland Islands',
                                      'United Kingdom',
                                      'Guinea Bissau',
                                      'Iran',
                                      'South Korea',
                                      'Kosovo',
                                      'Laos',
                                      'Moldova',
                                      'Macedonia',
                                      'North Korea',
                                      'Russia',
                                      'Republic of Serbia',
                                      'Swaziland',
                                      'Syria',
                                      'East Timor',
                                      'Venezuela',
                                      'Vietnam',
                                      'West Bank']

    countries = rename_countries(countries, list_of_countries_from_data, list_of_countries_from_geoJSON)

    countries = extend_geoJSON(cases, countries) #  extend geoJSON by COVID-19 data properties


    with open('new.geojson', 'w') as f:
        json.dump(countries, f)




    folium.Choropleth(
        geo_data=countries,
        name='choropleth COVID-19',
        data=cases,
        columns=['Name', option],
        key_on='feature.properties.name',
        fill_color='PuRd',
        nan_fill_color='white',
    ).add_to(map)












    # set style for geoJSON overlay to be transparent
    style = {'fillColor': '#00000000', 'color': '#00000000'}


    for country in countries['features']:
#        print(country['properties'])
        folium.GeoJson(
            data=country,
            tooltip=folium.GeoJsonTooltip(
                fields=aliases_for_geoJSON_tooltips(country['properties']['name'], cases),
                aliases=aliases_for_geoJSON_tooltips(country['properties']['name'], cases)
    ),
            style_function=lambda x: style
        ).add_to(map)





    html_map=map._repr_html_()

    return html_map
