import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import folium
from flask import Flask, render_template, Blueprint, Response, send_file
from matplotlib.figure import Figure
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def plot_options():
    data_url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'

    data = pd.read_csv(data_url, delimiter=',', header=0, quotechar='"', encoding="utf8", parse_dates=['date'])
    data.head()

    options = data.columns.values


    return options

def countries_list():
    data_url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'

    data = pd.read_csv(data_url, delimiter=',', header=0, quotechar='"', encoding="utf8", parse_dates=['date'])
    data.head()

    countries = data[['location']]
    countries = countries.drop_duplicates(subset=['location'], keep='first')
    countries = countries.values.tolist()

    flatten = lambda t: [item for sublist in t for item in sublist]
    countries = flatten(countries)

    return countries

def process_data(country):
    data_url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'

    data = pd.read_csv(data_url, delimiter=',', header=0, quotechar='"', encoding="utf8", parse_dates=['date'])
    data.head()

    data = data[data['location'] == country]
    data.head()

    return data


def generate_plots(country, data, options):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 12))

    ax1.plot(data['date'], data[options[0]])
    # Set title and labels for axes
    ax1.set(xlabel="Date (YYYY-MM)", ylabel=options[0], title=options[0]+ ' in ' + country)
    ax1.grid()
    ax1.fill_between(data['date'], data[options[0]], color=(185 / 255, 206 / 255, 255 / 255, 255 / 255))
    ax1.set_ylim(ax1.get_ylim())

    ax2.plot(data['date'], data[options[1]], color='black')
    # Set title and labels for axes
    ax2.set(xlabel="Date (YYYY-MM)", ylabel=options[1], title=options[1] + ' in ' + country)
    ax2.grid()
    ax2.fill_between(data['date'], data[options[1]], color=(0 / 255, 0 / 255, 0 / 255, 50 / 255))
    ax2.set_ylim(ax2.get_ylim())

    ax3.plot(data['date'], data[options[2]])
    # Set title and labels for axes
    ax3.set(xlabel="Date (YYYY-MM)", ylabel=options[2], title=options[2] + ' in ' + country)
    ax3.grid()
    ax3.fill_between(data['date'], data[options[2]], color=(185 / 255, 206 / 255, 255 / 255, 255 / 255))
    ax3.set_ylim(ax3.get_ylim())

    ax4.plot(data['date'], data[options[3]], color='black')
    # Set title and labels for axes
    ax4.set(xlabel="Date (YYYY-MM)", ylabel=options[3], title=options[3] + ' in ' + country)
    ax4.grid()
    ax4.fill_between(data['date'], data[options[3]], color=(0 / 255, 0 / 255, 0 / 255, 50 / 255))
    ax4.set_ylim(ax4.get_ylim())




    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return img









