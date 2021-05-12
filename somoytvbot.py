from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
PATH = "C:\Program Files (x86)\chromedriver.exe"

def addQuotes(oldString):
  newString = "\"" + oldString + "\""
  return newString

# def CSVSeperator():
#   return ","

address = "https://somoynews.tv/pages/details/267481/জঙ্গলে-বাঘের-মুখোমুখি-শচীন-%28ভিডিও%29"
driver = webdriver.Chrome(PATH)
driver.get(address)
try:
  element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "spc_d"))
  )
  # Removing ads
  iframes = driver.find_elements_by_tag_name("iframe")
  ads = len(iframes)
  if ads > 0:
    driver.execute_script("""
        var elems = document.getElementsByTagName("iframe"); 
        for(var i = 0, max = elems.length; i < max; i++)
          {
            elems[i].hidden=true;
          }
          """)
  title = driver.find_element_by_class_name("title").text
  link = address.rsplit("/",1)[0]
  metaKeys = driver.find_element_by_name("keywords").get_attribute("content")
  metaDesc = driver.find_element_by_name("description").get_attribute("content")
  reporter = driver.find_element_by_class_name("reporter").find_element_by_tag_name("a").text
  newsDesc = driver.find_element_by_class_name("spc_d").text
  publishingDate = driver.find_element_by_class_name("news-info").text
  publishingDate = publishingDate.split("\n",1)[1]

except:
    print("Error")
    
aString = addQuotes(title) + "," + \
  addQuotes(reporter) + "," + \
    addQuotes(publishingDate) + "," + \
      addQuotes(metaKeys) + "," + \
        addQuotes(metaDesc) + "," + \
          addQuotes(newsDesc) + "," + link + "," + str(ads)

file = open('clickbait_news_data.csv', mode='w+', encoding='utf-8')
file.write(aString)
file.close()
time.sleep(4)
driver.quit()