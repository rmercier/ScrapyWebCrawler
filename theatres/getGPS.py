import requests

def get_coordonates(address):

    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': address}
    r = requests.get(url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']

    gps = dict()
    gps['lat'] = location['lat']
    gps['lng'] = location['lng']

    return gps
