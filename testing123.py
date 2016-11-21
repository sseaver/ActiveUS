import googlemaps

gmaps = googlemaps.Client(key='AIzaSyA1oUv4FGoi_SFQ16BtK5huzJ0hUS_oDSc')

geocode_result = gmaps.geocode('1155 S Suber Rd, Greer, SC')

# reverse_geocode_result = gmaps.reverse_geocode((34.84799, -82.38395))

# print(reverse_geocode_result[0]['formatted_address'])

lat_lng_dict = geocode_result[0]['geometry']['location']

latitude = lat_lng_dict['lat']
longitude = lat_lng_dict['lng']

print(latitude, longitude)
