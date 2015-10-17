import collections
from flask import render_template, request
from FAS import app
from FAS.API import API



def setup_page_dict():
    """Make a dictionary of all the pages in the file for links at the top of
    the web page. Add the name and address of every new page here"""
    page_dict = collections.OrderedDict()
    page_dict['Home'] = '/'
    return page_dict

@app.route('/', methods=['GET', 'POST'])
def index_page():
    if request.method == 'GET':
        return render_template('home.html', title='Home',
                               page_dict=setup_page_dict(),
                               app_name=app.config['APP_NAME'])


    elif request.method == 'POST':
        latitude_form = request.form['latitude']
        longitude_form = request.form['longitude']
        user_query = API.LoadStations()
        stations = user_query.find_closest_bike(latitude_form, longitude_form)

        if request.form['which'] == "Bike":
            return render_template('results.html', title='Home',
                                   page_dict=setup_page_dict(),
                                   app_name=app.config['APP_NAME'],
                                   stations=stations,
                                   latitude_form = latitude_form,
                                   longitude_form = longitude_form,
                                   query = "Bikes")
        elif request.form['which'] == "Dock":
            return render_template('results.html', title='Home',
                                    page_dict=setup_page_dict(),
                                    app_name=app.config['APP_NAME'],
                                    stations=stations,
                                    latitude_form = latitude_form,
                                    longitude_form = longitude_form,
                                    query = "Docks")