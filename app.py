from flask import Flask, render_template, Blueprint, request, redirect, url_for, send_file
#  from first import first, html_map
from website.plots import generate_plots, process_data, countries_list, plot_options
from website import create_app
from website.world_map import world_map_options_list, create_world_map

countries = countries_list()
options = world_map_options_list()
options_for_plots = plot_options()

app = create_app()


@app.route('/')
def index():
    try:
        world_map = create_world_map(option=option_for_world_map)
    except:
        world_map = create_world_map()
    return render_template('index.html', countries=countries, options=options, options_for_plots=options_for_plots, world_map=world_map)


@app.route('/plots')
def plots():
    return render_template('plots.html', countries=countries, options_for_plots=options_for_plots, options=options)

@app.route('/create_plots')
def create_plots():
    data = process_data(country=country)
    plot = generate_plots(country=country, data=data, options=opts)
    return send_file(plot, mimetype='img/png')


@app.route('/get_country_for_plots', methods=['GET', 'POST'])
def get_country_for_plots():
    global country
    global opts
    opts = []
    country = request.form['Country']
    opts.clear()
    for i in range(4):
        opts.append(request.form['Option' + str(i)])
    return redirect(url_for('plots'))



@app.route('/get_option_for_map', methods=['GET', 'POST'])
def get_option_for_map():
    global option_for_world_map
    option_for_world_map = request.form['Get_option_for_map']
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)