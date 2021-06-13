from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time

allNews =""
count = 0

def addQuotes(oldString):
  newString = "\"" + oldString + "\""
  return newString

def makeCSV(name):
  global allNews
  file = open(f'{name}.csv', mode='w+', encoding='utf-8')
  file.write(allNews)
  file.close()

def getData(address):
  global allNews
  global count
  driver2 = webdriver.Chrome(PATH)
  driver2.get(address)
  try:
    element = WebDriverWait(driver2, 15).until(
      EC.presence_of_element_located((By.CLASS_NAME, "container"))
    )
    # Removing ads
    iframes = driver2.find_elements_by_tag_name("iframe")
    ads = len(iframes)
    if ads > 0:
      driver2.execute_script("""
          var elems = document.getElementsByTagName("iframe"); 
          for(var i = 0, max = elems.length; i < max; i++)
            {
              elems[i].hidden=true;
            }
            """)
    title = driver2.find_element_by_name("title").get_attribute("content")
    # link = address
    # metaKeys = driver2.find_element_by_name("keywords").get_attribute("content")
    metaKeys = 'N/A'
    metaDesc = driver2.find_element_by_name("description").get_attribute("content")
    reporter = driver2.find_element_by_css_selector(".pa-0.ma-0.text-md-h6.col.col-6").text
    publishingDate = driver2.find_element_by_css_selector(".d-inline.button").text
    publishingDate = publishingDate.split(",",1)[1]
    category = driver2.find_element_by_css_selector('.button.primary--text.cursor-pointer').text
    newsDescList = driver2.find_elements_by_class_name("description")
    newsDesc = ''
    for para in newsDescList:
        newsDesc += para.text
  except Exception as e:
      print(e)
  driver2.quit()

  aString = address + "," + \
    addQuotes(title) + "," + \
      addQuotes(reporter) + "," + \
        addQuotes(category) + "," + \
          addQuotes(publishingDate) + "," + \
            addQuotes(metaKeys) + "," + \
              addQuotes(metaDesc) + "," + \
                addQuotes(newsDesc) + "," + str(ads) + '\n'
  allNews += aString
  count += 1
  print("total news added", count)


if __name__ == '__main__':
  # Initializing chrome driver in selenium bot
  PATH = "C:\Program Files (x86)\chromedriver.exe"
  driver = webdriver.Chrome(PATH)

  # Adress of SomoyTV news category 
  site = "https://www.somoynews.tv/categories/%E0%A6%AC%E0%A6%BE%E0%A6%A3%E0%A6%BF%E0%A6%9C%E0%A7%8D%E0%A6%AF"
  driver.get(site)

  # Loading all the news
  time.sleep(5)
  while True:
    time.sleep(1)
    try: 
      element = driver.find_element_by_css_selector(".my-4.white--text.button.v-btn.v-btn--contained.v-btn--rounded.theme--light.v-size--default.primary")
      driver.execute_script("arguments[0].click();", element)
    except:
      break

  # Making list of the links of news found on the page
  newsList = driver.find_elements_by_css_selector(".white--text.button.px-2.ml-n2.v-btn.v-btn--flat.v-btn--router.v-btn--text.theme--light.v-size--default.red--text")

  # file = open('test.txt', mode='w+', encoding='utf-8')
  # listToStr = ' '.join(map(str, newsList))
  # file.write(listToStr)
  # file.close()

  for news in newsList:
    address = news.get_attribute("href")
    print(address)
    getData(address)

  makeCSV('somoyTVTechnology')

  time.sleep(10)
  driver.quit()