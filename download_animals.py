"""
Downloads clear single-animal photos from Wikipedia thumbnail API.
"""
import urllib.request
import urllib.parse
import json
import os
import time

UA = {'User-Agent': 'EducationalQuizGame/1.0 (idanatiya@outlook.com; educational non-commercial)'}

def wiki_thumb(title, width=600):
    p = urllib.parse.urlencode({'action':'query','titles':title,'prop':'pageimages','pithumbsize':width,'format':'json'})
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

def download(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        print(f'  skip (exists {os.path.getsize(path)//1024}KB)')
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
        print(f'  saved {len(data)//1024}KB')
        return True
    except Exception as e:
        print(f'  error: {e}')
        return False

os.makedirs('images/animals', exist_ok=True)

# (filename, [article candidates in order of preference])
items = [
    ('dog.jpg',      ['Labrador Retriever', 'Golden Retriever', 'Dog']),
    ('cat.jpg',      ['Domestic short-haired cat', 'Cat']),
    ('lion.jpg',     ['Lion']),
    ('elephant.jpg', ['African bush elephant', 'African elephant', 'Elephant']),
    ('giraffe.jpg',  ['Giraffe']),
    ('zebra.jpg',    ['Plains zebra', 'Zebra']),
    ('tiger.jpg',    ['Bengal tiger', 'Tiger']),
    ('bear.jpg',     ['Brown bear', 'Polar bear']),
    ('monkey.jpg',   ['Chimpanzee', 'Rhesus macaque', 'Monkey']),
    ('horse.jpg',    ['Horse']),
    ('cow.jpg',      ['Holstein Friesian cattle', 'Dairy cattle', 'Cattle']),
    ('pig.jpg',      ['Domestic pig', 'Pig']),
    ('chicken.jpg',  ['Chicken']),
    ('sheep.jpg',    ['Sheep', 'Domestic sheep']),
    ('rabbit.jpg',   ['European rabbit', 'Rabbit', 'Domestic rabbit']),
    ('duck.jpg',     ['Mallard', 'Duck']),
    ('owl.jpg',      ['Barn owl', 'Great horned owl', 'Owl']),
    ('penguin.jpg',  ['Emperor penguin', 'Penguin']),
    ('dolphin.jpg',  ['Bottlenose dolphin', 'Common dolphin', 'Dolphin']),
    ('frog.jpg',     ['Red-eyed tree frog', 'Frog']),
]

failed = []
for filename, articles in items:
    path = f'images/animals/{filename}'
    name = filename.replace('.jpg','')
    print(f'{name}...')
    got = False
    for article in articles:
        url = wiki_thumb(article, 600)
        if url:
            print(f'  {article}: {url[:80]}')
            if download(url, path):
                got = True
                break
        time.sleep(3)
    if not got:
        failed.append(name)
        print(f'  FAILED')
    time.sleep(5)

print('\n=== RESULTS ===')
for f in sorted(os.listdir('images/animals')):
    path = f'images/animals/{f}'
    size = os.path.getsize(path)
    print(f'  {"OK" if size > 15000 else "SMALL?"} {f}: {size//1024}KB')

if failed:
    print(f'\nFailed: {failed}')
else:
    print('\nAll OK!')
