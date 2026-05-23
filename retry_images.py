import urllib.request
import urllib.parse
import json
import os
import time

headers = {'User-Agent': 'EducationalQuizGame/1.0 (educational; non-commercial)'}

def get_wiki_thumb(title, size=500):
    params = urllib.parse.urlencode({'action':'query','titles':title,'prop':'pageimages','pithumbsize':size,'format':'json'})
    url = f'https://en.wikipedia.org/w/api.php?{params}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        for page in data['query']['pages'].values():
            if 'thumbnail' in page:
                return page['thumbnail']['source']
    except Exception as e:
        print(f'  API error: {e}')
    return None

def download(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 5000:
        print(f'  skip (exists)')
        return True
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        if len(data) < 5000:
            print(f'  too small ({len(data)} bytes)')
            return False
        with open(path, 'wb') as f:
            f.write(data)
        print(f'  saved {len(data)//1024}KB')
        return True
    except Exception as e:
        print(f'  download error: {e}')
        return False

items = [
    ('images/veg/corn.jpg',           'Maize'),
    ('images/veg/cauliflower.jpg',    'Cauliflower'),
    ('images/veg/sweetpotato.jpg',    'Sweet potato'),
    ('images/veg/asparagus.jpg',      'Asparagus'),
    ('images/veg/spinach.jpg',        'Spinach'),
    ('images/veg/peas.jpg',           'Pea'),
    ('images/veg/radish.jpg',         'Radish'),
    ('images/veg/celery.jpg',         'Celery'),
    ('images/vehicles/car.jpg',       'Car'),
    ('images/vehicles/bus.jpg',       'Bus'),
    ('images/vehicles/truck.jpg',     'Semi-trailer truck'),
    ('images/vehicles/ambulance.jpg', 'Ambulance'),
    ('images/vehicles/firetruck.jpg', 'Fire apparatus'),
    ('images/vehicles/motorcycle.jpg','Motorcycle'),
    ('images/vehicles/taxi.jpg',      'Taxi'),
    ('images/vehicles/jeep.jpg',      'Jeep'),
    ('images/vehicles/racecar.jpg',   'Formula One car'),
    ('images/vehicles/bicycle.jpg',   'Bicycle'),
    ('images/vehicles/tractor.jpg',   'Tractor'),
    ('images/vehicles/pickup.jpg',    'Pickup truck'),
    ('images/vehicles/subway.jpg',    'New York City Subway'),
]

for path, title in items:
    if os.path.exists(path) and os.path.getsize(path) > 5000:
        print(f'skip: {title}')
        continue
    print(f'{title}...')
    url = get_wiki_thumb(title)
    if url:
        print(f'  {url[:80]}...')
        download(url, path)
    else:
        print(f'  not found')
    time.sleep(5)

print('Done.')
