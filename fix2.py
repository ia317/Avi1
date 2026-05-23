"""
Targeted fix for remaining bad/missing images.
Uses Wikipedia thumbnail API with long delays to avoid rate limits.
"""
import urllib.request
import urllib.parse
import json
import os
import time
import hashlib

UA = {'User-Agent': 'EducationalQuizGame/1.0 (idanatiya@outlook.com; educational non-commercial)'}

def wiki_thumb(article, width=600):
    p = urllib.parse.urlencode({'action':'query','titles':article,'prop':'pageimages','pithumbsize':width,'format':'json'})
    req = urllib.request.Request(f'https://en.wikipedia.org/w/api.php?{p}', headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        for page in data['query']['pages'].values():
            if 'thumbnail' in page:
                return page['thumbnail']['source']
    except Exception as e:
        print(f'  API error: {e}')
    return None

def commons_url(filename, width=600):
    m = hashlib.md5(filename.encode('utf-8')).hexdigest()
    name = filename
    if filename.lower().endswith('.svg'):
        name = filename + '.png'
    return f'https://upload.wikimedia.org/wikipedia/commons/thumb/{m[0]}/{m[:2]}/{urllib.parse.quote(filename)}/{width}px-{urllib.parse.quote(name)}'

def download(url, path, force=False):
    if not force and os.path.exists(path) and os.path.getsize(path) > 10000:
        print(f'  skip (exists, {os.path.getsize(path)//1024}KB)')
        return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            data = r.read()
        if len(data) < 8000:
            print(f'  too small ({len(data)} bytes)')
            return False
        with open(path, 'wb') as f:
            f.write(data)
        print(f'  saved {len(data)//1024}KB -> {path}')
        return True
    except Exception as e:
        print(f'  error: {e}')
        return False

def try_wiki(path, articles, force=False):
    for article in articles:
        print(f'  trying Wikipedia: {article}')
        url = wiki_thumb(article, 600)
        if url:
            print(f'  got URL: {url[:80]}')
            if download(url, path, force=force):
                return True
        time.sleep(20)
    return False

def try_commons(path, filenames, force=False):
    for fn in filenames:
        url = commons_url(fn, 600)
        print(f'  trying Commons: {fn[:60]}')
        if download(url, path, force=force):
            return True
        time.sleep(20)
    return False

os.makedirs('images/veg', exist_ok=True)
os.makedirs('images/vehicles', exist_ok=True)

print('=== Fix missing/broken images ===\n')

# 1. Asparagus — missing
print('1. asparagus')
if not (os.path.exists('images/veg/asparagus.jpg') and os.path.getsize('images/veg/asparagus.jpg') > 10000):
    ok = try_wiki('images/veg/asparagus.jpg', ['Asparagus', 'Asparagus officinalis'], force=True)
    if not ok:
        ok = try_commons('images/veg/asparagus.jpg', [
            'Asparagus_2.jpg',
            'Asparagi.jpg',
            'Asparagus_officinalis_LC0102.jpg',
        ], force=True)
    if not ok:
        print('  FAILED - will remove from quiz')
else:
    print('  already OK')
time.sleep(20)

# 2. Fire truck — missing
print('2. firetruck')
if not (os.path.exists('images/vehicles/firetruck.jpg') and os.path.getsize('images/vehicles/firetruck.jpg') > 10000):
    ok = try_wiki('images/vehicles/firetruck.jpg', ['Fire engine', 'Fire apparatus', 'Fire truck'], force=True)
    if not ok:
        ok = try_commons('images/vehicles/firetruck.jpg', [
            'Boerne_Fire_Truck.jpg',
            'FDNY_Engine_55.jpg',
            'US_Air_Force_Fire_Truck.jpg',
        ], force=True)
    if not ok:
        print('  FAILED - will remove from quiz')
else:
    print('  already OK')
time.sleep(20)

# 3. Modern car
print('3. car (modern)')
ok = try_wiki('images/vehicles/car.jpg', ['Toyota Corolla (E210)', 'Honda Civic (tenth generation)', 'Volkswagen Golf Mk7'], force=True)
if not ok:
    try_commons('images/vehicles/car.jpg', [
        'Toyota_Corolla_E210_sedan_4_.jpg',
        'Volkswagen_Golf_VII_Comfortline_2.0_TDI_BlueMotion_Technology_DSG_Tiefseeblau_Metallic_Frontansicht_19._Oktober_2013_Velbert.jpg',
        'Kia_Optima_III_2013.jpg',
    ], force=True)
time.sleep(20)

# 4. Motor scooter (Vespa type)
print('4. scooter (motor/Vespa)')
ok = try_wiki('images/vehicles/scooter.jpg', ['Vespa', 'Motor scooter', 'Piaggio'], force=True)
if not ok:
    try_commons('images/vehicles/scooter.jpg', [
        'Piaggio_Vespa_GTS_Super_Sport_-_Flickr_-_Alexandre_Prévot_(9).jpg',
        'Vespa_GTS_300_Super.jpg',
        'Honda_PCX_2021.jpg',
    ], force=True)
time.sleep(20)

# 5. Carrot — single
print('5. carrot (single)')
ok = try_wiki('images/veg/carrot.jpg', ['Carrot'], force=True)
if not ok:
    try_commons('images/veg/carrot.jpg', [
        'Daucus_carota_subsp._sativus.jpg',
        'Karotte.jpg',
        'Carrot_Daucus_carota_root_closeup.jpg',
    ], force=True)
time.sleep(20)

# 6. Garlic — real photo
print('6. garlic (real photo)')
ok = try_wiki('images/veg/garlic.jpg', ['Garlic'], force=True)
if not ok:
    try_commons('images/veg/garlic.jpg', [
        'Garlic_6_filtered.jpg',
        'Allium_sativum_2.jpg',
        'Garlic_White_Background.jpg',
    ], force=True)

print('\n=== RESULTS ===')
for folder in ['images/veg', 'images/vehicles']:
    for f in sorted(os.listdir(folder)):
        path = f'{folder}/{f}'
        size = os.path.getsize(path)
        status = 'OK' if size > 15000 else 'SMALL?'
        print(f'  [{status}] {path}: {size//1024}KB')
