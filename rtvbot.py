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
  driver2 = webdriver.Chrome(PATH)
  driver2.get(address)
  try:
    element = WebDriverWait(driver2, 30).until(
      EC.presence_of_element_located((By.CLASS_NAME, "dtl_section"))
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
  ads = 2
  title = driver2.find_element_by_tag_name("h1").text
  link = address.rsplit("/",1)[0]
  metaKeys = driver2.find_element_by_name("keywords").get_attribute("content")
  metaDesc = driver2.find_element_by_name("description").get_attribute("content")
  category = driver2.find_element_by_class_name("breadcrumb").find_element_by_class_name("child").find_element_by_tag_name("a").text
  category = category.strip()
  # reporter = driver.find_element_by_xpath("//*[@class='rpt_name mt-2']").text
  try:
    reporter = driver2.find_element_by_css_selector('.rpt_name.mt-2').text
  except:
    reporter =""
  publishingDate = driver2.find_element_by_class_name("rpt_name.border-top.mt-1.pt-1").text
  # publishingDate = publishingDate.split("\n",1)[1]
  publishingDate = publishingDate.split(",",1)[0].strip()
  # print(publishingDate)
  paraList = driver2.find_element_by_class_name("dtl_section").find_elements_by_tag_name("p")
  newsDesc = ""
  for para in paraList:
    newsDesc += para.text + " "
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
  for i in range(30,100):
    site = f"https://www.rtvonline.com/all-news/?pg={i}"
    driver.get(site)
    time.sleep(2)
    # Making list of the links of news found on the page
    newsList = driver.find_elements_by_class_name("all_news_content")
    print(newsList)
    for news in newsList:
      address = news.get_attribute("href")
      print(address)
      getData(address)

    makeCSV('rtvnews')

  time.sleep(10)
  driver.quit()