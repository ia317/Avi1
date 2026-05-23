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

os.makedirs('images/veg', exist_ok=True)
os.makedirs('images/vehicles', exist_ok=True)

items = [
    # vegetables
    ('images/veg/carrot.jpg',      'Carrot'),
    ('images/veg/cucumber.jpg',    'Cucumber'),
    ('images/veg/tomato.jpg',      'Tomato'),
    ('images/veg/potato.jpg',      'Potato'),
    ('images/veg/onion.jpg',       'Onion'),
    ('images/veg/garlic.jpg',      'Garlic'),
    ('images/veg/pepper.jpg',      'Bell pepper'),
    ('images/veg/eggplant.jpg',    'Eggplant'),
    ('images/veg/zucchini.jpg',    'Zucchini'),
    ('images/veg/broccoli.jpg',    'Broccoli'),
    ('images/veg/cabbage.jpg',     'Cabbage'),
    ('images/veg/lettuce.jpg',     'Lettuce'),
    ('images/veg/corn.jpg',        'Corn'),
    ('images/veg/cauliflower.jpg', 'Cauliflower'),
    ('images/veg/sweetpotato.jpg', 'Sweet potato'),
    ('images/veg/asparagus.jpg',   'Asparagus'),
    ('images/veg/spinach.jpg',     'Spinach'),
    ('images/veg/peas.jpg',        'Pea'),
    ('images/veg/radish.jpg',      'Radish'),
    ('images/veg/celery.jpg',      'Celery'),
    # vehicles
    ('images/vehicles/car.jpg',        'Automobile'),
    ('images/vehicles/bus.jpg',        'Bus'),
    ('images/vehicles/truck.jpg',      'Truck'),
    ('images/vehicles/ambulance.jpg',  'Ambulance'),
    ('images/vehicles/firetruck.jpg',  'Fire engine'),
    ('images/vehicles/motorcycle.jpg', 'Motorcycle'),
    ('images/vehicles/taxi.jpg',       'Taxicab'),
    ('images/vehicles/policecar.jpg',  'Police car'),
    ('images/vehicles/jeep.jpg',       'Sport utility vehicle'),
    ('images/vehicles/racecar.jpg',    'Racing car'),
    ('images/vehicles/van.jpg',        'Van'),
    ('images/vehicles/train.jpg',      'Train'),
    ('images/vehicles/airplane.jpg',   'Airplane'),
    ('images/vehicles/helicopter.jpg', 'Helicopter'),
    ('images/vehicles/ship.jpg',       'Ship'),
    ('images/vehicles/scooter.jpg',    'Kick scooter'),
    ('images/vehicles/bicycle.jpg',    'Bicycle'),
    ('images/vehicles/tractor.jpg',    'Tractor'),
    ('images/vehicles/pickup.jpg',     'Pickup truck'),
    ('images/vehicles/subway.jpg',     'Rapid transit'),
]

failed = []
for path, title in items:
    print(f'{title}...')
    url = get_wiki_thumb(title)
    if url:
        print(f'  {url}')
        ok = download(url, path)
        if not ok:
            failed.append((path, title))
    else:
        print(f'  no image found')
        failed.append((path, title))
    time.sleep(2)

print(f'\nDone. Failed: {len(failed)}')
for p, t in failed:
    print(f'  {t} -> {p}')
