import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from os import path
import time
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

def addQuotes(oldString):
    newString = "\"" + oldString + "\""
    return newString

sg.theme('DarkAmber')
col  = [[ sg.Text(size=(135,50), key='-news-')]]
layout = [[sg.Text("URL input: "), sg.Input(key='-IN-'), sg.Checkbox('Clickbait', key="-clickbaitCheck-", size=(12, 1), default=True), sg.Button('Scrap'), sg.Button('Add to CSV'), sg.Button('Close'), sg.Text(size=(20,1), text_color="#3ad282", key="-message-")], \
    [sg.Text("Title: "), sg.Text(size=(120,1), key='-title-')], \
        [sg.Text("Meta Keys: "), sg.Text(size=(120,1), key='-metaKeys-')], \
            [sg.Text("Meta Description: "), sg.Text(size=(120,3), key='-metaDesc-')], \
                [sg.Text("Report Desk: "), sg.Text(size=(25,1), key='-reporter-'), sg.Text("Time: "), sg.Text(size=(20,1), key='-time-'), sg.Text("Category: "), sg.Text(size=(20,1), key='-category-'), sg.Text("Ads: "), sg.Text(size=(5,1), key='-ads-'), sg.Text("Clickbait: "), sg.Text(size=(5,1), key='-clickbait-')], \
                    [sg.Text("Link: "), sg.Text(size=(120,1), key='-link-')], \
                        [sg.Text("Full news: ")], \
                            [sg.Column(col, size=(1100,300), scrollable=True)]]


window = sg.Window("SomoyTV Manual Scrapper", layout)

while True:
    event, values = window.read()
    if event is None or event == 'Close':
        break
    address = values['-IN-']
    driver.get(address)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "container"))
        )
    except Exception as e:
        print(e)
        driver.close()
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
    title = driver.find_element_by_name("title").get_attribute("content")
    link = address
    # metaKeys = 'driver.find_element_by_name("keywords").get_attribute("content")'
    metaKeys = 'N/A'
    metaDesc = driver.find_element_by_name("description").get_attribute("content")
    reporter = driver.find_element_by_css_selector(".pa-0.ma-0.text-md-h6.col.col-6").text
    publishingDate = driver.find_element_by_css_selector(".d-inline.button").text
    publishingDate = publishingDate.split(",",1)[1]
    category = driver.find_element_by_css_selector('.button.primary--text.cursor-pointer').text
    newsDescList = driver.find_elements_by_class_name("description")
    newsDesc = ''
    for para in newsDescList:
        newsDesc += para.text
    clickbait = values['-clickbaitCheck-']
    
    window['-title-'].update(title)
    window['-metaKeys-'].update(metaKeys)
    window['-metaDesc-'].update(metaDesc)
    window['-reporter-'].update(reporter)
    window['-ads-'].update(ads)
    window['-category-'].update(category)
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
        if path.exists('somoytv.csv'):
            file = open('somoytv.csv', mode='a', encoding='utf-8')
        else:
            file = open('somoytv.csv', mode='w+', encoding='utf-8')
        file.write(aString)
        file.close()
        window['-message-'].update("Successfully Added!")
    else: 
        window['-message-'].update("")

window.close()
driver.close()

