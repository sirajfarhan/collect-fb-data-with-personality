import pandas as pd
import os
import json
import numpy as np

# import seaborn as sns
# import matplotlib.pyplot as plt
# sns.set(style="ticks", color_codes=True)

data = pd.read_csv("profiles.csv")
data = data.drop("Unnamed: 0",axis=1)
data = data.sample(data.shape[0])
data['url_id'] = data.url.str.replace('https://www.facebook.com/', '')

files = os.listdir("profiles")
files = [f.replace(".json","") for f in files]

data = data[data.url_id.isin(files)]

for index, row in data.iterrows():
    with open("profiles/" + row['url_id']  + ".json") as f:
        d = json.load(f)
    data.loc[index, 'friends'] = int(d['friends'].split()[0]) if 'friends' in d else None
    data.loc[index, 'profile_id'] = d['profile_id'] if 'profile_id' in d else None
    data.loc[index, 'gender'] = d['gender'] if 'gender' in d else None
    data.loc[index, 'current_city'] = d['current city'] if 'current city' in d else None
    data.loc[index, 'home_town'] = d['home town'] if 'home town' in d else None
    if 'religious views' in d:
        print(d['religious views'])
        if type(d['religious views']) is list:
            data.loc[index, 'religious_views'] = d['religious views'][0] if len(d['religious views']) > 0 else None
        else:
            data.loc[index, 'religious_views'] = d['religious views']
    if 'relationship' in d:
        if type(d['relationship']) is list:
            data.loc[index, 'relationship'] = d['relationship'][1]
        else:
            data.loc[index, 'relationship'] = d['relationship']
    else:
        data.loc[index, 'relationship'] = None

data.relationship = data.relationship.apply(lambda x: x.split()[0] if (x is not None) and ('since' in x) else x )

data['ie'] = np.where(data.personality.str[0] == 'i','introvert','extrovert')
data['ns'] = np.where(data.personality.str[1] == 'n','intuition','sensing')
data['tf'] = np.where(data.personality.str[2] == 't','thinking','feeling')
data['jp'] = np.where(data.personality.str[3] == 'j','judging','perceiving')


sns.catplot(x="ns", y="friends", data=data);
plt.show()
