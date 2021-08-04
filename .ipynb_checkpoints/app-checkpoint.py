#!/Users/jocelynrodal_1/opt/miniconda3/envs/geo_env/bin python 3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 18:13:09 2021

@author: jocelyn
"""
#/usr/bin/env python3
import streamlit as st
import os
import dill
import bokeh as b
import bokeh.plotting as bp
import datetime
import pandas as pd


#os.chdir('/Users/jocelynrodal_1/Dropbox/coding/tdi/capstone/data')
ny = dill.load(open('nyforceinjuriesdates.pkd', 'rb'))


st.title('Police Use of Force Data:')
st.title('A Localized Approach')

address = st.text_input('Type in your address to learn about use of force incidents at your local precinct')

if address:
    st.markdown('Your local precinct is: {}'.format(precinct))
    
    st.write('In the past 5 years:')
    st.write('Precinct 73 has reported {} uses of force and {} subject injuries in police encounters.'.format(p73forcecount, p73injurycount))
    #st.write('and {} subject injuries in police encounters'.format(p73injurycount))
    st.write('In 2019, one person was killed in a police encounter in precinct 73. His name was Kwesi Ashun.')
    st.write('Precinct 73 appears to use force more often than we would expect, given crime levels and population density.')
    
    st.bokeh_chart(pforce)
    st.bokeh_chart(pinjuries)
    
    
    
precinct73force = precinct73[precinct73['forcetype'].notnull()]
y1force = precinct73force.groupby(['date']).count()['forcetype']
xforce = precinct73force.groupby(['date']).count().reset_index()['date']


nyUoFinjuries['date'] = list(map(quartertodatetime, nyUoFinjuries['year'], 
                              nyUoFinjuries['quarter']))

nyUoFforceprecincts = nyUoFinjuries[(nyUoFinjuries['forcetype'].notnull()) & 
                                   (nyUoFinjuries['precinct'].notnull())]
y2force = nyUoFforceprecincts.groupby(['date']).count()['forcetype']/77

pforce = bp.figure(title="Reported Use of Force Incidents", 
              x_axis_type='datetime', 
              y_axis_label='Uses of Force')
pforce.line(xforce, y1force, legend_label='Precent 73', line_color='red')
pforce.line(xforce, y2force, legend_label='NYPD Average', line_color='blue')


precinct73injuries = precinct73[precinct73['injury'].notnull()]
y1injuries = precinct73injuries.groupby(['date']).count()['injury']
xinjuries = precinct73injuries.groupby(['date']).count().reset_index()['date']

nyUoFinjuriesprecincts = nyUoFinjuries[(nyUoFinjuries['injury'].notnull()) & 
                                   (nyUoFinjuries['precinct'].notnull())]
y2injuries = nyUoFinjuriesprecincts.groupby(['date']).count()['injury']/77

pinjuries = bp.figure(title="Injuries Reported from Police Encounters", 
              x_axis_type='datetime', 
              y_axis_label='Injuries')
pinjuries.line(xinjuries, y1injuries, legend_label='Precent 73', line_color='red')
pinjuries.line(xinjuries, y2injuries, legend_label='NYPD Average', line_color='blue')


p73forcecount = sum(y1force)
p73injurycount = sum(y1injuries)

    
    