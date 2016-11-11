import googlemaps

gmaps = googlemaps.Client(key='AIzaSyA1oUv4FGoi_SFQ16BtK5huzJ0hUS_oDSc')

geocode_result = gmaps.geocode('101 N Main Street, Greenville, SC')

reverse_geocode_result = gmaps.reverse_geocode((34.85216, -82.29121))

print(geocode_result, reverse_geocode_result)
