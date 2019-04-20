 existing_ids = ['basic-info','bio','contact-info','education','family','living','nicknames','quote','relationship','skills','work','years-overview']

items = document.getElementsByClassName("_55wo _2xfb _1kk1")

html = document.body.innerHTML
firstIndex = html.indexOf('currentProfileID')
html = html.slice(firstIndex)
html = html.slice(0,html.indexOf("prefilledValue"))
profile_id = html.replace('currentProfileID:','').replace(',','')

data = {}
links_to_detail = []

var currentURL = location.protocol + '//' + location.host + location.pathname

data['profile_id'] = profile_id

for (var i = 0; i < items.length; i++) {
  if(existing_ids.includes(items[i].id)) {
    for (var j = 0; j < items[i].children[1].children.length; j++) {
      item = items[i].children[1].children[j].innerText.split("\n")
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
    let section = items[i].innerText.split("\n")[0].toLowerCase()
    links_to_detail.push(section)
  }
}


section_ids = {
 'check-ins': 302324425790,
 'sports': 330076653784935,
 'music': 221226937919712,
 'films': 177822289030932,
 'tv programmes': 309918815775486,
 'books': 332953846789204,
 'apps and games': '249944898349166:58',
 'likes': 2409997254,
 'events': 2344061033,
 'reviews': 254984101287276,
 'videos': 1560653304174514
}


url_path_with_name = ['friends','photos']

for (var i = 0; i < links_to_detail.length; i++) {
  section = links_to_detail[i]
  if(url_path_with_name.includes(section)) {
    // links_to_detail.push(currentURL.replace('about',section))
  } else {
    if(section_ids[section])
      window.location = `https://m.facebook.com/timeline/app_section/?section_token=${profile_id}:${section_ids[section]}`
  }
}
