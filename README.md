

Track My Precinct

This app delivers localized information on police use of force in NYC's five boroughs. The goal is to allow residents to understand police violence on a neighborhood-by-neighborhood basis.

http://trackmyprecinct.herokuapp.com/

Author: Jocelyn Rodal

Data Sources:
Data on police use of force and civilian injuries comes from the NYPD:
https://www1.nyc.gov/site/nypd/stats/reports-analysis/use-of-force-data.page

Data on police killings comes from The Washington Post Police Shootings Database and from Mapping Police Violence:
https://www.washingtonpost.com/graphics/investigations/police-shootings-database/
https://mappingpoliceviolence.org/

Geocoding is from Open Street Map:
https://www.openstreetmap.org/

NYPD precinct geography from NYC OpenData
https://data.cityofnewyork.us/Public-Safety/Police-Precincts/78dh-3ptz

Data Processing:
The NYPD delivered their data on use of force and civilian injuries in a series of several dozen excel files. Combining all of those together into one pandas dataframe was labor-intensive. To give a fuller picture, I then added in police killings data from the Washington Post and Mapping Police Violence (hand-checking the handful of killings that were in one database but not the other). I have not normalized or otherwise altered this data in any way; I have chosen simply to present this data as the NYPD recorded it.

It is important to note that the NYPD's definition of a use of force may not line up with the definitions used by the public and by individual citizens: as such, it is hard to vouch for the absolute accuracy of the numbers of use-of-force incidents reported. However, because the NYPD's standards for what qualifies as a use of force are uniform from one precinct to the next, comparative numbers between precincts should be much more accurate. As such, I encourage users to rely on this data primarily for comparative purposes.
