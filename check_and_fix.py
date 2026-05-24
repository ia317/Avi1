"""
Checks all quiz images. Re-downloads any that are drawings (SVG-based) or missing.
Fetches Wikipedia URLs lazily with delays to avoid rate limiting.
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
        print(f'      API error: {e}')
    return None

def commons_url(filename, width=600):
    enc = filename.replace(' ', '_')
    m = hashlib.md5(enc.encode('utf-8')).hexdigest()
    name = enc + '.png' if enc.lower().endswith('.svg') else enc
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
            return f'small({len(data)}b)'
        with open(path, 'wb') as f:
            f.write(data)
        return f'saved {len(data)//1024}KB'
    except Exception as e:
        return f'error: {e}'

# Source types: ('wiki', article_title) or ('commons', filename)
# Each item: (image_path, is_force, [(type, value), ...])
# is_force=True  -> always re-download (known bad)
# is_force=False -> skip if file exists and is large; re-download only if SVG thumbnail

ITEMS = [
    # FRUITS
    ('images/apple.jpg',         False, [('wiki','Gala (apple)'), ('wiki','Apple')]),
    ('images/banana.jpg',        False, [('wiki','Cavendish banana'), ('wiki','Banana')]),
    ('images/orange.jpg',        False, [('wiki','Navel orange'), ('wiki','Orange (fruit)')]),
    ('images/strawberry.jpg',    False, [('wiki','Strawberry')]),
    ('images/watermelon.jpg',    False, [('wiki','Watermelon')]),
    ('images/pineapple.jpg',     False, [('wiki','Pineapple')]),
    ('images/mango.jpg',         False, [('wiki','Alphonso (mango)'), ('wiki','Mango')]),
    ('images/lemon.jpg',         False, [('commons','Lemon-Whole-Split.jpg'), ('wiki','Lemon')]),
    ('images/cherry.jpg',        False, [('wiki','Cherry')]),
    ('images/grapes.jpg',        False, [('wiki','Grape')]),
    ('images/peach.jpg',         False, [('wiki','Peach')]),
    ('images/kiwi.jpg',          False, [('wiki','Kiwifruit')]),
    ('images/pear.jpg',          False, [('wiki','Pear')]),
    ('images/pomegranate.jpg',   False, [('wiki','Pomegranate')]),
    ('images/avocado.jpg',       False, [('wiki','Avocado')]),
    ('images/plum.jpg',          False, [('wiki','Plum')]),
    ('images/blueberry.jpg',     False, [('wiki','Blueberry')]),
    ('images/raspberry.jpg',     False, [('wiki','Raspberry')]),
    ('images/apricot.jpg',       False, [('wiki','Apricot')]),
    ('images/date.jpg',          False, [('wiki','Medjool'), ('commons','Dates_on_white_background.jpg'), ('wiki','Date palm')]),
    ('images/fig.jpg',           False, [('wiki','Common fig'), ('commons','Ficus_carica.jpg')]),
    ('images/pricklypear.jpg',   False, [('wiki','Prickly pear'), ('commons','Opuntia_ficus_indica_fruit.jpg')]),
    ('images/loquat.jpg',        False, [('wiki','Loquat')]),
    ('images/persimmon.jpg',     False, [('wiki','Persimmon')]),
    ('images/guava.jpg',         False, [('wiki','Guava')]),
    ('images/grapefruit.jpg',    False, [('wiki','Grapefruit')]),
    ('images/nectarine.jpg',     False, [('wiki','Nectarine')]),
    # VEGETABLES
    ('images/veg/carrot.jpg',    True,  [('commons','Carrot_Daucus_carota_root_closeup.jpg'), ('wiki','Carrot')]),
    ('images/veg/cucumber.jpg',  False, [('wiki','Cucumber')]),
    ('images/veg/tomato.jpg',    False, [('wiki','Tomato')]),
    ('images/veg/potato.jpg',    False, [('wiki','Potato')]),
    ('images/veg/onion.jpg',     False, [('wiki','Onion')]),
    ('images/veg/garlic.jpg',    True,  [('commons','Allium_sativum_2.jpg'), ('commons','Garlic_6_filtered.jpg'), ('commons','Garlic_White_Background.jpg')]),
    ('images/veg/pepper.jpg',    False, [('wiki','Bell pepper')]),
    ('images/veg/eggplant.jpg',  False, [('wiki','Eggplant')]),
    ('images/veg/zucchini.jpg',  False, [('wiki','Zucchini')]),
    ('images/veg/broccoli.jpg',  False, [('wiki','Broccoli')]),
    ('images/veg/cabbage.jpg',   False, [('wiki','Cabbage')]),
    ('images/veg/lettuce.jpg',   False, [('wiki','Lettuce')]),
    ('images/veg/corn.jpg',      False, [('wiki','Corn on the cob')]),
    ('images/veg/cauliflower.jpg',False,[('wiki','Cauliflower')]),
    ('images/veg/sweetpotato.jpg',False,[('wiki','Sweet potato')]),
    ('images/veg/asparagus.jpg', True,  [('wiki','Asparagus'), ('commons','Asparagus_2.jpg'), ('commons','Asparagi.jpg')]),
    ('images/veg/spinach.jpg',   False, [('wiki','Spinach')]),
    ('images/veg/peas.jpg',      False, [('wiki','Pea')]),
    ('images/veg/radish.jpg',    False, [('wiki','Radish')]),
    ('images/veg/celery.jpg',    False, [('wiki','Celery')]),
    # VEHICLES (only known-bad ones)
    ('images/vehicles/car.jpg',       True, [('wiki','Toyota Corolla (E210)'), ('wiki','Honda Civic (tenth generation)'), ('wiki','Volkswagen Golf Mk7')]),
    ('images/vehicles/firetruck.jpg',  True, [('wiki','Fire engine'), ('wiki','Fire apparatus')]),
    ('images/vehicles/scooter.jpg',    True, [('wiki','Vespa'), ('wiki','Motor scooter')]),
]

fixed, skipped, failed = [], [], []

for path, force, sources in ITEMS:
    name = os.path.basename(path)
    exists = os.path.exists(path) and os.path.getsize(path) > 10000

    if not force and exists:
        # Quick check: get the wikipedia thumb URL for the first wiki source
        # to see if it's SVG-based (drawing/diagram)
        first_wiki = next((v for t, v in sources if t == 'wiki'), None)
        if first_wiki:
            url = wiki_thumb(first_wiki)
            time.sleep(2)
            if url and '.svg' not in url.lower():
                print(f'ok  {path} ({os.path.getsize(path)//1024}KB)')
                skipped.append(path)
                continue
            elif url and '.svg' in url.lower():
                print(f'SVG {path} -> will fix')
                force = True
            # If url is None (API error), skip to be safe
            else:
                print(f'ok  {path} (API gave None, keeping existing)')
                skipped.append(path)
                continue
        else:
            skipped.append(path)
            continue

    print(f'FIX {path}')
    ok = False
    for stype, sval in sources:
        if stype == 'wiki':
            url = wiki_thumb(sval)
            label = f'wiki:{sval}'
        else:
            url = commons_url(sval)
            label = f'commons:{sval}'

        if not url:
            time.sleep(4)
            continue

        print(f'    {label[:60]}')
        r = download(url, path, force=True)
        print(f'    -> {r}')
        if r.startswith('saved'):
            ok = True
            break
        time.sleep(8)

    if ok:
        fixed.append(path)
    else:
        failed.append(path)

print(f'\n=== DONE ===')
print(f'Fixed:   {len(fixed)}')
print(f'Skipped: {len(skipped)}')
print(f'Failed:  {len(failed)}')
for f in failed:
    print(f'  FAIL: {f}')
