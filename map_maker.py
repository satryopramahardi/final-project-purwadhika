print('Starting...')

#Import essentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import axes
import seaborn as sns
import folium 

#geojson file on city community area borders
geojson_file = 'chicago-community-areas.geojson'

import warnings
warnings.filterwarnings("ignore")


print('Reading files...')
#Import the file
df = pd.read_csv('Crimes_-_2018.csv').dropna()
df.columns

df = df[['ID','Case Number','Date','Block','IUCR','Primary Type', 'Description', 'Location Description', 'Arrest', 'Domestic', 'Beat',
       'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
       'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude']]

#Only include crime mentioned above
sos = ['THEFT','HOMICIDE','CRIM SEXUAL ASSAULT','ASSAULT','ROBBERY','BURGLARY','MOTOR VEHICLE THEFT','ARSON','BATTERY','CRIMINAL TRESPASS']
serious_crime = df[df['Primary Type'].isin(sos)]
serious_crime = serious_crime.drop(['Year'],axis=1)

#Reformat date time information for easier processing
from datetime import datetime
serious_crime.Date = serious_crime.Date.apply(lambda x: datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p'))

#Give a day-night flag to distinguish crimes happening
serious_crime['DayFlag'] = (serious_crime['Date'].dt.hour > 7) & (serious_crime['Date'].dt.hour < 19)

#create month column
serious_crime.insert(len(serious_crime.columns),'Month',serious_crime['Date'].dt.month)

serious_crime.to_csv('serious_crime.csv',index=False)

#Saving city location for later mapping use
median_lat=serious_crime['Latitude'].median()
median_long=serious_crime['Longitude'].median()
center_coordinate = [median_lat,median_long]

from sklearn.cluster import OPTICS, cluster_optics_dbscan
import joblib
clust_100 = joblib.load('100_cluster_model.pickle')

print('Processing Map...')
ca =[]
community_names=['Rogers Park','West Ridge','Uptown','Lincoln Square','North Center','Lake View','Lincoln Park','Near North Side',
                'Edison Park','Norwood Park','Jefferson Park','Forest Glen','North Park','Albany Park','Portage Park',
                'Irving Park','Dunning','Montclare','Belmont Cragin','Hermosa','Avondale','Logan Square','Humboldt Park',
                'West Town','Austin','West Garfield Park','East Garfield Park','Near West Side','North Lawndale','South Lawndale',
                'Lower West Side','Loop','Near South Side','Armour Square','Douglas','Oakland','Fuller Park','Grand Boulevard',
                'Kenwood','Washington Park','Hyde Park','Woodlawn','South Shore','Chatham','Avalon Park','South Chicago','Burnside',
                'Calumet Heights','Roseland','Pullman','South Deering','East Side','West Pullman','Riverdale','Hegewisch','Garfield Ridge',
                'Archer Heights','Brighton Park','McKinley Park','Bridgeport','New City','West Elsdon','Gage Park','Clearing','West Lawn',
                'Chicago Lawn','West Englewood','Englewood','Greater Grand Crossing','Ashburn','Auburn Gresham','Beverly','Washington Heights',
                'Mount Greenwood','Morgan Park',"OHare",'Edgewater']


for i in range(1,len(serious_crime.groupby('Community Area'))+1):
    months =[]
    for month,crimes in serious_crime.groupby('Month'):
        months.append(len(crimes))
    ca_data = {
        'Community Area':i,
        'Community Name':community_names[i-1].upper(),
        'Latitude': serious_crime[serious_crime['Community Area']==i]['Latitude'].median(),
        'Longitude': serious_crime[serious_crime['Community Area']==i]['Longitude'].median(),
        'Number of Crimes': len(serious_crime[serious_crime['Community Area']==i]),
        'Monthly': months
    }

    ca.append(ca_data)
ca_df = pd.DataFrame(ca)
ca_df.to_csv("community_areas.csv",index=False)

X = serious_crime[['Latitude','Longitude']]
X['label']=clust_100.labels_



# circles = pd.DataFrame(columns=['labels','value','lat','lon'])
# circles['labels'] = X['label'].value_counts().index
# circles['value'] = X['label'].value_counts().values

# circles = circles.sort_values(by = 'labels')
# circles = circles.reset_index()
# circles = circles.drop(['index'],axis=1)

# for i in range(0,len(circles)):
#     idx = circles.iloc[i,0]
#     median_lat = X[X['label']==idx]['Latitude'].median()
#     median_lon = X[X['label']==idx]['Longitude'].median()
#     circles.iloc[i,2] = median_lat
#     circles.iloc[i,3] = median_lon

print('Creating map...')
# chicago_basemap = folium.Map(location=center_coordinate,zoom_start=12)
# folium.GeoJson(
#     geojson_file,
#     name='chicago_basemap'
# ).add_to(chicago_basemap)

# for row in ca_df.itertuples() :
#     folium.Marker([row[3],row[4]],
#         tooltip=f"{row[2]} ({row[1]})",
#         popup=f"Crime: {row[6]}",
#         icon = folium.Icon(color='green', icon='info-sign')).add_to(chicago_basemap)


# chicago_coropleth = folium.Map(location=center_coordinate,zoom_start=10)
# folium.Choropleth(
#     geo_data=geojson_file,
#     name='choropleth',
#     data=ca_df,
#     columns=['Community Name', 'Number of Crimes'],
#     key_on='feature.properties.community',
#     fill_color='OrRd',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Crime Rate'
# ).add_to(chicago_coropleth)


# # from folium.plugins import HeatMap

# clustered_map = folium.Map(location=center_coordinate, tiles='CartoDB Positron',zoom_start=11)

# for i in range(1,len(circles)):
#   folium.Circle(
#     location=[float(circles.iloc[i]['lat']), float(circles.iloc[i]['lon'])],
# #     radius=float(circles.iloc[i]['value']*5),
#     radius = 100,
#     stroke = True, 
#     fill_color='blue',
#     fill=True
#   ).add_to(clustered_map)

# folium.GeoJson(
#     geojson_file,
#     name='chicago_basemap'
# ).add_to(clustered_map)


# from folium.plugins import HeatMap


# crime_map = folium.Map(location=center_coordinate, tiles='CartoDB Positron',zoom_start=11)
# val_max = int(circles.value.max())

# hm = folium.FeatureGroup('heatmap')
# heat_data = [[row['lat'],row['lon'],row['value']] for index, row in circles.iterrows()]
# HeatMap(heat_data, radius=50, max_val=val_max,min_opacity=0.3, max_zoom=13).add_to(hm)
# hm.add_to(crime_map)

# folium.GeoJson(
#     geojson_file,
#     name='geojson').add_to(crime_map)

# crl = folium.FeatureGroup()

# folium.LayerControl().add_to(crime_map)



print('Saving map...')
# chicago_basemap.save('maps/basemap.html')
# chicago_coropleth.save('maps/chicago_coropleth.html')
# clustered_map.save('maps/clustered_map.html')
# crime_map.save('maps/crime_map.html')
print('Done')