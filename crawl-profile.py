from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import pickle
import json
import os

import pandas as pd

driver = webdriver.Chrome()

cookies = pickle.load(open("cookies.pkl", "rb"))

data = pd.read_csv("dataset/profiles.csv", header=0)
# data = data.drop("Unnamed: 0",axis=1)
data = data.sample(data.shape[0])
data['url_id'] = data.url.str.replace('https://www.facebook.com/', '')

files = os.listdir("dataset/profiles")
files = [f.replace(".json","") for f in files]

data = data[~data.url_id.isin(files)]

url = 'https://m.facebook.com'

driver.get(url)

for cookie in cookies:
    driver.add_cookie(cookie)

time.sleep(1)

driver.refresh()

# driver.set_window_size(600, 5000)

for index, row in data.iterrows():
    fileName = row.url.replace('https://www.facebook.com/', '')
    profile_url = row.url.replace("https://www.","https://m.") + "/about"

    scolls = 0
    driver.get(profile_url)
    while True:
        driver.execute_script("window.scrollBy(0,1000)");
        time.sleep(2)
        scolls += 1

        if scolls == 7:
            break


    json_object = driver.execute_script("""
     existing_ids = ['basic-info','bio','contact-info','education','family','living','nicknames','quote','relationship','skills','work','years-overview']


    html = document.body.innerHTML
    firstIndex = html.indexOf('currentProfileID')
    html = html.slice(firstIndex)
    html = html.slice(0,html.indexOf("prefilledValue"))
    console.log("HTML",html)
    profile_id = html.replace('currentProfileID:','').replace('currentProfileID":','').replace(',','').replace('"','')
    console.log("profile_id",profile_id)
    data = {}
    data['profile_id'] = profile_id

    items = document.getElementsByClassName("_55wo _2xfb _1kk1")
    links_to_detail = []

    var currentURL = location.protocol + '//' + location.host + location.pathname

    for (var i = 0; i < items.length; i++) {
      if(existing_ids.includes(items[i].id)) {
        for (var j = 0; j < items[i].children[1].children.length; j++) {
          item = items[i].children[1].children[j].innerText.split("\\n")
          switch (items[i].id) {
            case 'basic-info':
            case 'contact-info':
            case 'living':
              key = item[item.length - 1].toLowerCase()
              item = item.slice(0, item.length - 1)
              item = item.length == 1 ? item[0] : item
              if(key == 'languages' || key == 'interested in') {
                item = item.split(/,|and/).map(it => it.trim().toLowerCase())
              }
              data[key] = item
            break;
            case 'bio':
            case 'relationship':
              data[items[i].id] = item.length == 1 ? item[0]: item
            break;
            case 'family':

            if(!data[items[i].id]) {
              data[items[i].id] = []
            }
            d = {}
            d[item[1].toLowerCase()] = item[0]
            data[items[i].id].push(d)
            break
            default:
            if(!data[items[i].id]) {
              data[items[i].id] = []
            }
            data[items[i].id].push(item)
          }

        }
      } else {
        let section = items[i].innerText.split("\\n")[0].toLowerCase()
        links_to_detail.push(section)
      }
    }

    return { data, links_to_detail }
    """)

    data = json_object['data']

    url_path_with_name = ['friends','photos']

    section_ids = {
      'check-ins': '302324425790:112',
      'sports people': '330076653784935:99',
      'sports team': '330076653784935:95',
      'music': '221226937919712',
      'films': '177822289030932',
      'tv programmes': '309918815775486',
      'books': '332953846789204',
      'apps and games': '249944898349166:58',
      'likes': '2409997254',
      'events': '2344061033',
      'reviews': '254984101287276',
      'videos': '1560653304174514'
     }

    class_names = {
        'music': 'item _1zq-',
        'reviews': 'item _1zq-',
        'sports people': '_1a5p',
        'sports team': '_1a5p',
        'films': '_5qk1',
        'tv programmes': '_5qk1',
        'books': '_5qk1',
        'apps and games': '_1a5p',
        'events': 'item _1zq-',
     }

    if 'photos' in json_object['links_to_detail']:
        json_object['links_to_detail'] = [link for link in json_object['links_to_detail'] if link != 'photos']
        json_object['links_to_detail'] = ['photos'] + json_object['links_to_detail']

    if 'sports' in json_object['links_to_detail']:
        json_object['links_to_detail'] = [link for link in json_object['links_to_detail'] if link != 'sports']
        json_object['links_to_detail'].append('sports people')
        json_object['links_to_detail'].append('sports team')


    for link in json_object['links_to_detail']:
        if link == 'friends':
            driver.get(profile_url.replace('about', 'friends'))
            time.sleep(2)
            data[link] = driver.execute_script("""
                return document.querySelector("#root > div.timeline > div.item._cs2.acw > a > div > div._4mo.c > div._4mp > span").textContent
            """)
        elif link == 'photos':
            data[link] = driver.execute_script("""
                links = []
                items = document.getElementsByClassName("_39pi _1mh- croppedPhotoGridItem _12xv")
                for(var i=0; i<items.length; i++) {
                    links.push(items[i].getAttribute("href"))
                }
                return links
            """)
        elif link in class_names:
            url = 'https://m.facebook.com/timeline/app_section/?section_token=' + str(data['profile_id']) + ':' + str(section_ids[link])
            driver.get(url)
            time.sleep(2)
            if link == 'music' or link == 'events' or link == 'reviews':
                music_scroll = 0
                while True:
                    driver.execute_script("window.scrollBy(0,3000)");
                    time.sleep(2)
                    music_scroll += 1

                    if music_scroll == 3:
                        break
            if link == 'films' or link == 'tv programmes' or link == 'books':
                see_more_button = driver.find_elements_by_class_name('primarywrap')
                while len(see_more_button) > 1:
                    try:
                        see_more_button[1].click()
                        time.sleep(2)
                        see_more_button = driver.find_elements_by_class_name('primarywrap')
                        driver.execute_script("window.scrollBy(0,3000)");
                    except Exception as e:
                        break

            if link in class_names:
                    script = """
                        links = []
                        items = document.getElementsByClassName('"""+ class_names[link]  + """')
                        for(var i = 0; i < items.length; i++) {
                            links.push(items[i].firstChild.getAttribute('href'))
                        }
                        return links
                        """
                    data[link] = driver.execute_script(script)
    fileName = fileName.replace('/','')
    with open('dataset/profiles/' + fileName + '.json', 'w') as f:
        f.write(json.dumps(data))
