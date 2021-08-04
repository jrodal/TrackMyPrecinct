#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 18:13:09 2021

@author: jocelyn
"""


import streamlit as st
import dill
import pandas as pd
import geopandas as gpd
from urllib.parse import quote
from urllib.request import urlopen
import simplejson as json
from shapely.geometry import Point
import bokeh as b
import bokeh.plotting as bp
from collections import defaultdict

#use st.cache to speed things up

#get dataframes
ny = dill.load(open('ny.pkd', 'rb'))
nykillings = dill.load(open('nywithkillings.pkd', 'rb'))
nyPrecincts = gpd.read_file('nypd_precincts.shp')
nyPrecincts['precinct'] = nyPrecincts['precinct'].astype(int)

location = None
precinct = None

#initial display
st.title('Track My Precinct')
st.header('Learn about Police Use of Force in _Your_ Neighborhood')

#get location for user address
address = st.text_input('Type in any address in the five boroughs of New York')
osmEndpoint = "http://nominatim.openstreetmap.org/search?q={}&addressdetails=1&format=json"
url = osmEndpoint.format(quote(address))
address_dict = json.loads(urlopen(url).read())
if len(address) != 0 and address_dict == []:
    location = None
    st.markdown("I'm sorry, I didn't understand that address, please try again.")
elif len(address) != 0 and address_dict != []:
    location = Point(float(address_dict[0]['lon']), float(address_dict[0]['lat']))

#once we have a location, get precinct
if location:
    try:
        rawprecinct = nyPrecincts[nyPrecincts['geometry'].contains(location)]['precinct'].iat[0]
        precinctDict = {18: 'Midtown North Precinct', 14: 'Midtown South Precinct', 
                        22: 'Central Park Precinct'}
        if rawprecinct in precinctDict:
            precinctname = precinctDict[rawprecinct]
            precinct = precinctDict[rawprecinct].replace(' Precinct', '')
        else: 
            precinctname = f'Precinct {rawprecinct}'
            precinct = rawprecinct
    except IndexError:
        st.markdown("That address doesn't appear to be covered by the NYPD. \
                    Unfortunately, right now I am only able to cover \
                    the five boroughs of New York City.")
        st.markdown("")
        precinct = None
    
#once we have a precinct, display information about it
if precinct:
    st.markdown(f'Your local precinct is: {precinct}')
    st.markdown('')
    
    #get data on use of force and injuries
    precinctData = ny[ny['precinct']==precinct]
    forceData = precinctData[precinctData['forcetype'].notnull()]
    forceTotal = forceData.shape[0]
    injuryData = precinctData[precinctData['injury'].notnull()]
    injuryTotal = injuryData.shape[0]
    forceMessage = f'In the past 5 years, {precinctname} has reported {forceTotal} ' + \
        f'uses of force and {injuryTotal} civilian injuries in police encounters.'
    
    #get killings data
    peoplekilled = list(nykillings[nykillings['precinct']==precinct]["Victim's name"])
    numkillings = len(peoplekilled)
    if numkillings == 0:
        killingsMessage = 'Since 2013, no one has been killed ' + \
            f'by police in {precinctname}.'
    elif numkillings == 1:
        gender = nykillings[nykillings['precinct']==precinct]["Victim's gender"].iat[0].strip()
        pronoundict = defaultdict(lambda: 'Their')
        pronoundict.update({'Male': 'His', 'Female': 'Her'})
        pronoun = pronoundict[gender]
        killingsMessage = 'Since 2013, one person has been killed by police ' + \
            f'in {precinctname}. {pronoun} name was {peoplekilled[0]}.'
    elif numkillings >= 2:
        if numkillings == 2:
            names = ' and '.join(peoplekilled)
        else:
            names = ', '.join(peoplekilled[:-1]) + ', and ' + peoplekilled[-1]
        killingsMessage = f'Since 2013, {numkillings} people have been killed ' + \
            f'by police in {precinctname}. Their names were {names}.'
    
    #prepare charts
    x = forceData.groupby(['date']).count().reset_index()['date']
    yforce = forceData.groupby(['date']).count()['forcetype']
    yinjury = injuryData.groupby(['date']).count()['injury']
    
    nyForcePrecincts = ny[(ny['forcetype'].notnull()) & (ny['precinct'].notnull())]
    y_avg_force = nyForcePrecincts.groupby(['date']).count()['forcetype']/77
    
    nyInjuryPrecincts = ny[(ny['injury'].notnull()) & (ny['precinct'].notnull())]
    y_avg_injury = nyInjuryPrecincts.groupby(['date']).count()['injury']/77
    
    pforce = bp.figure(title="Reported Use of Force Incidents", 
                       x_axis_type='datetime', 
                       y_axis_label='Uses of Force per quarter')
    pforce.line(x, yforce, legend_label=precinctname, line_color='red', line_width=1.5)
    pforce.line(x, y_avg_force, legend_label='NYPD Average', line_color='blue', line_width=1.5)
    pforce.y_range.start = 0

    pinjury = bp.figure(title="Civilian Injuries Reported from Police Encounters", 
                          x_axis_type='datetime', 
                          y_axis_label='Injuries per quarter')
    pinjury.line(x, yinjury, legend_label=precinctname, line_color='red', line_width=1.5)
    pinjury.line(x, y_avg_injury, legend_label='NYPD Average', line_color='blue', line_width=1.5)
    pinjury.y_range.start = 0
    
    #display data
    st.write(forceMessage)
    st.write(killingsMessage)
    st.bokeh_chart(pforce)
    st.bokeh_chart(pinjury)
    
 