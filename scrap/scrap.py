import json
import pandas as pd
from tqdm import tqdm
from helper import *

import seaborn as sns
import matplotlib.pyplot as plt

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

from google_play_scraper import Sort, reviews, app


sns.set(style='whitegrid', palette='muted', font_scale=1.2)

appList = [
    'com.blackboard.android.bbstudent', #blackboard 
    'com.byjus.tutorplus', #byjus
    'com.newsela.android', #newsela
    'com.mobile.simplilearn', #simplilearn
    'co.april2019.tcac' #class plus
]
app_infos = []

def print_json(json_object):
    json_str = json.dumps(
    json_object,
    indent=2,
    sort_keys=True,
    default=str
    )
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))

for ap in tqdm(appList):
    info = app(ap, lang='en', country='us')
    del info['comments']
    app_infos.append(info)

app_reviews = []

for ap in tqdm(appList):
  for score in list(range(1, 6)):
    for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
      rvs, _ = reviews(
        ap,
        lang='en',
        country='us',
        sort=sort_order,
        count= 200 if score <= 3 else 100,
        filter_score_with=score
      )
      for r in rvs:
        r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
        r['appId'] = ap
      app_reviews.extend(rvs)

print_json(app_reviews[0])
print(app_infos[0])
print(len(app_reviews))
app_reviews_df = pd.DataFrame(app_reviews)
app_reviews_df.to_csv('reviews.csv', index=None, header=True)