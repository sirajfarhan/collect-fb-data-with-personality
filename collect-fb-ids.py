from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import pickle
import json

driver = webdriver.Chrome()

# username = driver.find_element_by_xpath('//*[@id="email"]')
# username.send_keys("")
#
# password = driver.find_element_by_xpath('//*[@id="pass"]')
# password.send_keys("")
#
# login = driver.find_element_by_xpath('//*[@id="u_0_2"]')
# login.click()
#
# time.sleep(15)
#
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))


personality_types = ['intj','infj','istj','istp','isfp','isfj','infp','intp','entp','entj','enfj','enfp','estj','esfj','estp','esfp']
pages = ['personality','strengths-and-weaknesses','personality-and-emotions','relationships-dating','friends','parents','careers','at-work','conclusion']

base1 = 'https://www.facebook.com/plugins/feedback.php?app_id=326516237427150&channel=https%3A%2F%2Fstaticxx.facebook.com%2Fconnect%2Fxd_arbiter%2Fr%2Fj-GHT1gpo6-.js%3Fversion%3D43%23cb%3Dff050500%26domain%3Dwww.16personalities.com%26origin%3Dhttps%253A%252F%252Fwww.16personalities.com%252Ff62b65328%26relation%3Dparent.parent&container_width=1138&height=3000&href=http%3A%2F%2Fwww.16personalities.com%2F'
base2 = '&locale=en_US&sdk=joey&version=v2.10'

driver.set_script_timeout(500)

count = 0
cookies_added = False
for personality_type in personality_types:
    for page in pages:
        url = base1 + personality_type + '-' + page + base2 + '&pt=' + personality_type + '&pp=' + page
        driver.get(url)
        if not cookies_added:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            cookies_added = True
            driver.refresh()
        driver.execute_async_script("""
        var done = arguments[0];
        max = parseInt((parseInt(document.getElementsByClassName(" _50f7")[0].textContent.split(" ")[0]) / 10)) - 2

        async function main() {
            for (let i=1; i<max; i++) {
                console.log('CLICKED', i)
                let retry = 0
                while(true) {
                    try {
                        await clickButton()
                        break
                    } catch (e) {
                        await delay(1000)
                        retry++
                        if(retry == 5) break;
                    }
                }

            }
            actors = document.getElementsByClassName(' UFICommentActorName')

            data = []
            urlParams = new URLSearchParams(window.location.search);
            for(var i=0; i<actors.length; i++) {
                data.push({
                    'url': actors[i].getAttribute('href'),
                    'personality': urlParams.get('pt'),
                    'name': actors[i].text
                })
            }
            urlParams = new URLSearchParams(window.location.search)
            console.log(urlParams.get('pt') + '-' + urlParams.get('pp') + '.json')
            done(download(JSON.stringify(data), 'personality_profiling_' + urlParams.get('pt') + '_' + urlParams.get('pp') + '.json', 'application/json'))
        }


        function clickButton() {
          return new Promise((resolve, reject) => {
            button = document.getElementsByClassName('_1gl3 _4jy0 _4jy3 _517h _51sy _42ft')
            try {
                button[0].click()
            }catch(e) {
                reject(e)
            }
            setTimeout(resolve, 1000);
          });
        }

        function download(content, filename, contentType)
        {
            if(!contentType) contentType = 'application/octet-stream';
                var a = document.createElement('a');
                var blob = new Blob([content], {'type':contentType});
                a.href = window.URL.createObjectURL(blob);
                a.download = filename;
                a.click();
        }

        function delay(time) {
            return new Promise((resolve, reject) => {
                setTimeout(resolve, time);
            })
        }

        main()
        """)



# browser_log = driver.get_log('performance')
# events = [process_browser_log_entry(entry) for entry in browser_log]
# events = [event for event in events if 'Network.response' in event['method']]

# print(events)
