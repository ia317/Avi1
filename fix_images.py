"""
Downloads clear single-object photos from Wikimedia Commons.
Force-overwrites bad/missing images.
"""
import urllib.request
import urllib.parse
import json
import os
import time
import hashlib

UA = {'User-Agent': 'EducationalQuizGame/1.0 (educational non-commercial)'}

def commons_file_url(filename, width=500):
    """Build a Wikimedia Commons thumbnail URL from a file name."""
    m = hashlib.md5(filename.encode('utf-8')).hexdigest()
    name = filename
    if filename.lower().endswith('.svg'):
        name = filename + '.png'
    return f'https://upload.wikimedia.org/wikipedia/commons/thumb/{m[0]}/{m[:2]}/{filename}/{width}px-{name}'

def wikipedia_thumb(article, width=500):
    """Get thumbnail URL from a Wikipedia article."""
    p = urllib.parse.urlencode({'action':'query','titles':article,'prop':'pageimages','pithumbsize':width,'format':'json'})
    req = urllib.request.Request(f'https://en.wikipedia.org/w/api.php?{p}', headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        for page in data['query']['pages'].values():
            if 'thumbnail' in page:
                return page['thumbnail']['source']
    except Exception as e:
        print(f'    API error: {e}')
    return None

def download(url, path, force=False):
    if not force and os.path.exists(path) and os.path.getsize(path) > 5000:
        print(f'    skip (exists)')
        return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        if len(data) < 8000:
            print(f'    too small ({len(data)} bytes)')
            return False
        with open(path, 'wb') as f:
            f.write(data)
        print(f'    saved {len(data)//1024}KB')
        return True
    except Exception as e:
        print(f'    error: {e}')
        return False

def try_urls(path, urls, force=True):
    for url in urls:
        print(f'  trying {url[:70]}...')
        if download(url, path, force=force):
            return True
        time.sleep(2)
    return False

os.makedirs('images/veg', exist_ok=True)
os.makedirs('images/vehicles', exist_ok=True)

print('=== VEGETABLES ===')

# Carrot — single carrot on white background
print('carrot')
try_urls('images/veg/carrot.jpg', [
    commons_file_url('Daucus_carota_subsp._sativus.jpg'),
    commons_file_url('Carrot_2019-10-11.jpg'),
    commons_file_url('Karotte.jpg'),
], force=True)
time.sleep(3)

# Garlic — real photo, NOT botanical drawing
print('garlic')
try_urls('images/veg/garlic.jpg', [
    commons_file_url('Allium_sativum_(Garlic)_white_background.jpg'),
    commons_file_url('Garlic-Heads.jpg'),
    commons_file_url('Garlic_6_filtered.jpg'),
    commons_file_url('Garlic_single.jpg'),
], force=True)
time.sleep(3)

# Corn — real photo of corn on the cob
print('corn')
try_urls('images/veg/corn.jpg', [
    commons_file_url('Corn_on_the_cob.jpg'),
    commons_file_url('Corn_on_the_Cob.jpg'),
    commons_file_url('Corn-Maize_Zea_mays.jpg'),
], force=True)
time.sleep(3)

# Pepper — single clear bell pepper
print('pepper')
try_urls('images/veg/pepper.jpg', [
    commons_file_url('Red_and_Green_Pepper.jpg'),
    commons_file_url('Bell_pepper_red.jpg'),
    commons_file_url('Red_capsicum_and_cross_section.jpg'),
    commons_file_url('Fresh_Chili.jpg'),
], force=True)
time.sleep(3)

# Asparagus — bundle of asparagus spears
print('asparagus')
try_urls('images/veg/asparagus.jpg', [
    commons_file_url('Asparagus-bundle.jpg'),
    commons_file_url('Asparagus_bundle.jpg'),
    commons_file_url('White_asparagus.jpg'),
    commons_file_url('Green_Asparagus.jpg'),
], force=False)
time.sleep(3)

# Mushroom — replace asparagus if it still fails
print('mushroom (for asparagus fallback)')
try_urls('images/veg/mushroom.jpg', [
    commons_file_url('Agaricus_bisporus_(J.E.Lange)_Imbach,_1946.jpg'),
    commons_file_url('Mushroom_(Pleurotus_ostreatus).jpg'),
    commons_file_url('Portobello_mushroom.jpg'),
], force=False)
time.sleep(3)

print('\n=== VEHICLES ===')

# Car — modern car, not 1925 Model T
print('car')
try_urls('images/vehicles/car.jpg', [
    commons_file_url('2019_Toyota_Corolla_sedan_(facelift,_white),_front_7.31.19.jpg'),
    commons_file_url('2022_Toyota_Corolla_Hybrid_LE_(facelift)_front.jpg'),
    commons_file_url('2020_Honda_Civic_Sport_sedan,_front_7.9.20.jpg'),
    commons_file_url('Volkswagen_Golf_VI_front_20100516.jpg'),
], force=True)
time.sleep(3)

# Fire truck
print('firetruck')
try_urls('images/vehicles/firetruck.jpg', [
    commons_file_url('Boerne_Fire_Truck.jpg'),
    commons_file_url('FDNY_Tower_Ladder_117.jpg'),
    commons_file_url('Red_fire_engine_-_geograph.org.uk_-_564356.jpg'),
    commons_file_url('Firetruck_side.JPG'),
], force=False)
time.sleep(3)

# Scooter — motor scooter (Vespa type), NOT kick scooter
print('scooter (motor)')
try_urls('images/vehicles/scooter.jpg', [
    commons_file_url('Vespa_LX_125_white_background.jpg'),
    commons_file_url('Piaggio_Vespa.jpg'),
    commons_file_url('Honda_PCX150_(2018).jpg'),
    commons_file_url('Yamaha_N-Max_155_(2020).jpg'),
], force=True)
time.sleep(3)

# Check results
print('\n=== RESULTS ===')
missing = []
for folder in ['images/veg', 'images/vehicles']:
    for f in sorted(os.listdir(folder)):
        path = f'{folder}/{f}'
        size = os.path.getsize(path)
        status = 'OK' if size > 15000 else 'SMALL?'
        print(f'  [{status}] {path}: {size//1024}KB')
        if size < 8000:
            missing.append(path)

if missing:
    print(f'\nProblematic: {missing}')
else:
    print('\nAll images look OK!')
