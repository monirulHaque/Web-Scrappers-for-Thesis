import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

def addQuotes(oldString):
  newString = "\"" + oldString + "\""
  return newString

sg.theme('DarkAmber')
layout = [[sg.Text("URL input: "), sg.Input(key='-IN-'), sg.Checkbox('Clickbait', key="-clickbaitCheck-", size=(12, 1), default=True), sg.Button('Scrap'), sg.Button('Add to CSV'), sg.Button('Close'), sg.Text(size=(20,1), text_color="#3ad282", key="-message-")], \
    [sg.Text("Title: "), sg.Text(size=(120,1), key='-title-')], \
        [sg.Text("Meta Keys: "), sg.Text(size=(120,1), key='-metaKeys-')], \
            [sg.Text("Meta Description: "), sg.Text(size=(120,2), key='-metaDesc-')], \
                [sg.Text("Report Desk: "), sg.Text(size=(30,1), key='-reporter-'), sg.Text("Time: "), sg.Text(size=(20,1), key='-time-'), sg.Text("Ads: "), sg.Text(size=(5,1), key='-ads-'), sg.Text("Clickbait: "), sg.Text(size=(5,1), key='-clickbait-')], \
                    [sg.Text("Link: "), sg.Text(size=(120,1), key='-link-')], \
                        [sg.Text("Full news: ")], \
                            [sg.Text(size=(120,25), key='-news-')]]


window = sg.Window("SomoyTV Manual Scrapper", layout)

while True:
    event, values = window.read()
    if event is None or event == 'Close':
        break
    address = values['-IN-']
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
        clickbait = values['-clickbaitCheck-']
    except:
        driver.close()
    window['-title-'].update(title)
    window['-metaKeys-'].update(metaKeys)
    window['-metaDesc-'].update(metaDesc)
    window['-reporter-'].update(reporter)
    window['-ads-'].update(ads)
    window['-clickbait-'].update(clickbait)
    window['-time-'].update(publishingDate)
    window['-link-'].update(link)
    window['-news-'].update(newsDesc)
    if event == 'Add to CSV':

        aString = addQuotes(title) + "," + \
            addQuotes(reporter) + "," + \
                addQuotes(publishingDate) + "," + \
                    addQuotes(metaKeys) + "," + \
                        addQuotes(metaDesc) + "," + \
                            addQuotes(newsDesc) + "," + \
                                link + "," + str(ads) + "," + str(clickbait) + "\n"
        file = open('clickbait_news_data.csv', mode='a', encoding='utf-8')
        file.write(aString)
        file.close()
        window['-message-'].update("Successfully Added!")

window.close()
driver.close()

