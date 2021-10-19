from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import os.path
from os import path

allNews =""
count = 0

def addQuotes(oldString):
  newString = "\"" + oldString + "\""
  return newString

def makeCSV(name):
  global allNews
  if os.path.exists(f"{name}.csv"):
    file = open(f'{name}.csv', mode='a', encoding='utf-8')
  else:
    file = open(f'{name}.csv', mode='w+', encoding='utf-8')
  file.write(allNews)
  file.close()

def getData(address):
  global allNews
  global count
  driver2 = webdriver.Chrome(chrome_options=chrome_options, executable_path=PATH)
  driver2.get(address)
  try:
    element = WebDriverWait(driver2, 50).until(
      EC.presence_of_element_located((By.TAG_NAME, "p"))
    )
  except Exception as e:
    print(e)
  # Removing ads
  # iframes = driver2.find_elements_by_tag_name("iframe")
  # ads = len(iframes)
  # if ads > 0:
  #   driver2.execute_script("""
  #       var elems = document.getElementsByTagName("iframe"); 
  #       for(var i = 0, max = elems.length; i < max; i++)
  #         {
  #           elems[i].hidden=true;
  #         }
  #         """)
  try:
    ads = 1
    title = driver2.find_element_by_class_name("entry-title").text
    link = address
    metaKeys = 'N/A'
    metaDesc = 'N/A'
    category = 'N/A'
    reporter = 'N/A'
    publishingTime = driver2.find_element_by_xpath("//meta[@property='article:published_time']").get_attribute("content").split("T")
    publishingDate = publishingTime[0]
    # print(publishingDate)
    paraList = driver2.find_element_by_class_name("entry-content").find_elements_by_tag_name("p")
    newsDesc = ""
    for para in paraList:
        newsDesc += para.text + "\n"
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
  except Exception as e:
    print(e)
  print("total news added", count)


if __name__ == '__main__':
  # Initializing chrome driver in selenium bot
  chrome_options = webdriver.ChromeOptions()
  prefs = {"profile.managed_default_content_settings.images": 2}
  chrome_options.add_experimental_option("prefs", prefs)

  PATH = "C:\Program Files (x86)\chromedriver.exe"
  driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=PATH)

  # Adress of SomoyTV news category 
  for i in range(1,25):
    site = f"https://thebasenewz.com/page/{i}/"
    driver.get(site)
    time.sleep(2)

    # Making a list of the links of news found on the page
    newsList = driver.find_elements_by_class_name("entry-title")
    for news in newsList:
      address = news.find_element_by_tag_name("a").get_attribute("href")
      getData(address)

    makeCSV('thebasenewz')

  time.sleep(10)
  driver.quit()