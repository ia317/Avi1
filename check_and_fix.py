"""
Checks all quiz images for SVG-based thumbnails (= drawings/diagrams).
Re-downloads any drawing with a real photo alternative.
"""
import urllib.request
import urllib.parse
import json
import os
import time
import hashlib

UA = {'User-Agent': 'EducationalQuizGame/1.0 (idanatiya@outlook.com; educational non-commercial)'}

def wiki_thumb_url(article, width=600):
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

def commons_url(filename, width=600):
    enc = filename.replace(' ', '_')
    m = hashlib.md5(enc.encode('utf-8')).hexdigest()
    name = enc
    if enc.lower().endswith('.svg'):
        name = enc + '.png'
    return (f'https://upload.wikimedia.org/wikipedia/commons/thumb/'
            f'{m[0]}/{m[:2]}/{urllib.parse.quote(enc)}/{width}px-{urllib.parse.quote(name)}')

def download(url, path, force=True):
    if not force and os.path.exists(path) and os.path.getsize(path) > 10000:
        return 'skip'
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            data = r.read()
        if len(data) < 8000:
            return f'small({len(data)})'
        with open(path, 'wb') as f:
            f.write(data)
        return f'saved {len(data)//1024}KB'
    except Exception as e:
        return f'error: {e}'

def try_sources(path, sources, force=True):
    for label, url in sources:
        print(f'    try {label}: {url[:70]}')
        r = download(url, path, force)
        print(f'    -> {r}')
        if r.startswith('saved'):
            return True
        time.sleep(8)
    return False

# Each entry: (image_path, check_article, [(label, url_or_commons_fn), ...])
# check_article: the Wikipedia article to check for SVG thumbnail
# If thumbnail is SVG → try the real_photo_sources list
# Also force-replace known-bad items regardless of SVG check.

KNOWN_BAD = {
    'images/veg/garlic.jpg',    # confirmed Woodwill 1793 botanical drawing
    'images/veg/carrot.jpg',    # confirmed bundle of many carrots
    'images/veg/asparagus.jpg', # was missing
    'images/vehicles/firetruck.jpg',  # was missing
    'images/vehicles/car.jpg',        # was 1925 Model T
    'images/vehicles/scooter.jpg',    # was kick scooter board
}

items = [
    # FRUITS
    ('images/apple.jpg',        'Apple',           [('wiki:Gala (apple)', wiki_thumb_url('Gala (apple)')),
                                                    ('wiki:Apple',        wiki_thumb_url('Apple'))]),
    ('images/banana.jpg',       'Banana',          [('wiki:Cavendish banana', wiki_thumb_url('Cavendish banana')),
                                                    ('wiki:Banana',           wiki_thumb_url('Banana'))]),
    ('images/orange.jpg',       'Orange (fruit)',  [('wiki:Navel orange',     wiki_thumb_url('Navel orange')),
                                                    ('wiki:Orange (fruit)',    wiki_thumb_url('Orange (fruit)'))]),
    ('images/strawberry.jpg',   'Strawberry',      [('wiki:Strawberry',       wiki_thumb_url('Strawberry'))]),
    ('images/watermelon.jpg',   'Watermelon',      [('wiki:Watermelon',       wiki_thumb_url('Watermelon'))]),
    ('images/pineapple.jpg',    'Pineapple',       [('wiki:Pineapple',        wiki_thumb_url('Pineapple'))]),
    ('images/mango.jpg',        'Mango',           [('wiki:Alphonso (mango)', wiki_thumb_url('Alphonso (mango)')),
                                                    ('wiki:Mango',            wiki_thumb_url('Mango'))]),
    ('images/lemon.jpg',        'Lemon',           [('commons:Lemon-Whole-Split.jpg', commons_url('Lemon-Whole-Split.jpg')),
                                                    ('wiki:Lemon',                     wiki_thumb_url('Lemon'))]),
    ('images/cherry.jpg',       'Cherry',          [('wiki:Cherry',           wiki_thumb_url('Cherry'))]),
    ('images/grapes.jpg',       'Grape',           [('wiki:Grape',            wiki_thumb_url('Grape'))]),
    ('images/peach.jpg',        'Peach',           [('wiki:Peach',            wiki_thumb_url('Peach'))]),
    ('images/kiwi.jpg',         'Kiwifruit',       [('wiki:Kiwifruit',        wiki_thumb_url('Kiwifruit'))]),
    ('images/pear.jpg',         'Pear',            [('wiki:Pear',             wiki_thumb_url('Pear'))]),
    ('images/pomegranate.jpg',  'Pomegranate',     [('wiki:Pomegranate',      wiki_thumb_url('Pomegranate'))]),
    ('images/avocado.jpg',      'Avocado',         [('wiki:Avocado',          wiki_thumb_url('Avocado'))]),
    ('images/plum.jpg',         'Plum',            [('wiki:Plum',             wiki_thumb_url('Plum'))]),
    ('images/blueberry.jpg',    'Blueberry',       [('wiki:Blueberry',        wiki_thumb_url('Blueberry'))]),
    ('images/raspberry.jpg',    'Raspberry',       [('wiki:Raspberry',        wiki_thumb_url('Raspberry'))]),
    ('images/apricot.jpg',      'Apricot',         [('wiki:Apricot',          wiki_thumb_url('Apricot'))]),
    ('images/date.jpg',         'Medjool',         [('wiki:Medjool',          wiki_thumb_url('Medjool')),
                                                    ('commons:Dates_on_white_background.jpg', commons_url('Dates_on_white_background.jpg'))]),
    ('images/fig.jpg',          'Common fig',      [('wiki:Common fig',       wiki_thumb_url('Common fig')),
                                                    ('commons:Ficus_carica.jpg', commons_url('Ficus_carica.jpg'))]),
    ('images/pricklypear.jpg',  'Prickly pear',    [('wiki:Prickly pear',     wiki_thumb_url('Prickly pear')),
                                                    ('commons:Opuntia_ficus_indica_fruit.jpg', commons_url('Opuntia_ficus_indica_fruit.jpg'))]),
    ('images/loquat.jpg',       'Loquat',          [('wiki:Loquat',           wiki_thumb_url('Loquat'))]),
    ('images/persimmon.jpg',    'Persimmon',       [('wiki:Persimmon',        wiki_thumb_url('Persimmon'))]),
    ('images/guava.jpg',        'Guava',           [('wiki:Guava',            wiki_thumb_url('Guava'))]),
    ('images/grapefruit.jpg',   'Grapefruit',      [('wiki:Grapefruit',       wiki_thumb_url('Grapefruit'))]),
    ('images/nectarine.jpg',    'Nectarine',       [('wiki:Nectarine',        wiki_thumb_url('Nectarine'))]),
    # VEGETABLES
    ('images/veg/carrot.jpg',   'Carrot',          [('commons:Carrot_Daucus_carota_root_closeup.jpg', commons_url('Carrot_Daucus_carota_root_closeup.jpg')),
                                                    ('wiki:Carrot',           wiki_thumb_url('Carrot'))]),
    ('images/veg/cucumber.jpg', 'Cucumber',        [('wiki:Cucumber',         wiki_thumb_url('Cucumber'))]),
    ('images/veg/tomato.jpg',   'Tomato',          [('wiki:Tomato',           wiki_thumb_url('Tomato'))]),
    ('images/veg/potato.jpg',   'Potato',          [('wiki:Potato',           wiki_thumb_url('Potato'))]),
    ('images/veg/onion.jpg',    'Onion',           [('wiki:Onion',            wiki_thumb_url('Onion'))]),
    ('images/veg/garlic.jpg',   'Garlic',          [('commons:Allium_sativum_2.jpg', commons_url('Allium_sativum_2.jpg')),
                                                    ('commons:Garlic_6_filtered.jpg', commons_url('Garlic_6_filtered.jpg')),
                                                    ('commons:Garlic_White_Background.jpg', commons_url('Garlic_White_Background.jpg'))]),
    ('images/veg/pepper.jpg',   'Bell pepper',     [('wiki:Bell pepper',      wiki_thumb_url('Bell pepper'))]),
    ('images/veg/eggplant.jpg', 'Eggplant',        [('wiki:Eggplant',         wiki_thumb_url('Eggplant'))]),
    ('images/veg/zucchini.jpg', 'Zucchini',        [('wiki:Zucchini',         wiki_thumb_url('Zucchini'))]),
    ('images/veg/broccoli.jpg', 'Broccoli',        [('wiki:Broccoli',         wiki_thumb_url('Broccoli'))]),
    ('images/veg/cabbage.jpg',  'Cabbage',         [('wiki:Cabbage',          wiki_thumb_url('Cabbage'))]),
    ('images/veg/lettuce.jpg',  'Lettuce',         [('wiki:Lettuce',          wiki_thumb_url('Lettuce'))]),
    ('images/veg/corn.jpg',     'Corn on the cob', [('wiki:Corn on the cob',  wiki_thumb_url('Corn on the cob'))]),
    ('images/veg/cauliflower.jpg','Cauliflower',   [('wiki:Cauliflower',      wiki_thumb_url('Cauliflower'))]),
    ('images/veg/sweetpotato.jpg','Sweet potato',  [('wiki:Sweet potato',     wiki_thumb_url('Sweet potato'))]),
    ('images/veg/asparagus.jpg','Asparagus',       [('wiki:Asparagus',        wiki_thumb_url('Asparagus')),
                                                    ('commons:Asparagus_2.jpg', commons_url('Asparagus_2.jpg')),
                                                    ('commons:Asparagi.jpg',    commons_url('Asparagi.jpg'))]),
    ('images/veg/spinach.jpg',  'Spinach',         [('wiki:Spinach',          wiki_thumb_url('Spinach'))]),
    ('images/veg/peas.jpg',     'Pea',             [('wiki:Pea',              wiki_thumb_url('Pea'))]),
    ('images/veg/radish.jpg',   'Radish',          [('wiki:Radish',           wiki_thumb_url('Radish'))]),
    ('images/veg/celery.jpg',   'Celery',          [('wiki:Celery',           wiki_thumb_url('Celery'))]),
    # VEHICLES - only the known-bad ones
    ('images/vehicles/car.jpg',       'Car',        [('wiki:Toyota Corolla (E210)', wiki_thumb_url('Toyota Corolla (E210)')),
                                                     ('wiki:Honda Civic (tenth generation)', wiki_thumb_url('Honda Civic (tenth generation)')),
                                                     ('wiki:Volkswagen Golf Mk7', wiki_thumb_url('Volkswagen Golf Mk7'))]),
    ('images/vehicles/firetruck.jpg', 'Fire engine',[('wiki:Fire engine',      wiki_thumb_url('Fire engine')),
                                                     ('wiki:Fire apparatus',    wiki_thumb_url('Fire apparatus'))]),
    ('images/vehicles/scooter.jpg',   'Vespa',      [('wiki:Vespa',            wiki_thumb_url('Vespa')),
                                                     ('wiki:Motor scooter',    wiki_thumb_url('Motor scooter'))]),
]

print(f'Checking {len(items)} images...\n')
fixed = []
skipped = []
failed = []

for path, check_label, sources in items:
    # Check current thumb URL for this item
    check_url = None
    for label, url in sources:
        if url and not label.startswith('commons:'):
            check_url = url
            break

    is_bad = path in KNOWN_BAD

    if not is_bad and check_url:
        is_svg = '.svg' in check_url.lower()
        if is_svg:
            print(f'DRAWING: {path} ({check_label})')
            is_bad = True
        elif os.path.exists(path) and os.path.getsize(path) > 10000:
            print(f'ok      {path} ({os.path.getsize(path)//1024}KB)')
            skipped.append(path)
            continue

    if is_bad or not os.path.exists(path) or os.path.getsize(path) < 10000:
        if is_bad:
            print(f'FIX     {path}')
        else:
            print(f'MISSING {path}')
        if try_sources(path, sources):
            fixed.append(path)
        else:
            failed.append(path)

print(f'\n=== DONE ===')
print(f'Fixed: {len(fixed)}')
print(f'Skipped (already OK): {len(skipped)}')
print(f'Failed: {len(failed)}')
for f in failed:
    print(f'  FAIL: {f}')
