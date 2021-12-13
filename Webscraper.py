

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 11:05:27 2021
# this is a data science project
@author: leon
"""
import time
import pandas
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
#create list in steps by 10 to adjust the url
numbers_list = list()
all_judgements = list()
for i in range(9):
    numbers_list.append(i*10)
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
from webdriver_manager.chrome import ChromeDriverManager
d = webdriver.Chrome(ChromeDriverManager().install())
links = list()
#access all pages containing weblinks to the judgements
for x in numbers_list[0:10]:
	
    elements = []
    url = 'https://openjur.de/suche/Flüchtlingseigenschaft/-fg-og-sg-vf/' + str(x) + '.vd-desc.html'
    d.get(url)
    #get the href of all elements leading to the judgement pages
    #elements.append(d.find_elements_by_class_name("card-header"))
    #print(elements)
    for elem in d.find_elements_by_xpath('/html/body/div/div/div[1]/div[*]/div[1]/div/div[2]/a'):
        links.append(elem.get_attribute('href'))
        print(links)
import itertools
#access all links stored in the previous steps
# code snippets partly from: https://stackoverflow.com/questions/24775988/how-to-navigate-to-a-new-webpage-in-selenium
final_list = list()
h2s = list()
for link in links:
    #page = requests.get(link).content
    #soup = BeautifulSoup(page, 'lxml')
    d.get(link)
    soup = BeautifulSoup(d.page_source, "lxml")
    time.sleep(1) 
    try:
    		#extract only the text part from the websites
            full_content = soup.body.find("div", {'id': "econtent"})
            h6s = full_content.find_all('h6')
            structured_data=[]
            for h6 in h6s:
                temp_data = []
                for tag in h6.next_siblings:
                    if tag.name == 'h6':
                        break
                    #elif tag.name == 'p':
                    elif tag.name == 'p':
                        temp_data.append(tag.get_text())
                structured_data.append(temp_data)
            #print(structured_data[0])
    #except:
        	#print('No findings.')
            #assign structured data to different datasets
            tenor = structured_data[0]
            tatbestand = structured_data[1]
            gruende = structured_data[2]
            final_list.append([link,tenor,tatbestand,gruende])
            #print(link)
            #print(final_list[0])
    except:
        	print('No findings.')
print(final_list)
judgements_df = pandas.DataFrame(final_list, columns=['Link','Tenor','Tatbestand','Gruende'])
print(judgements_df)
structured_data.clear()
judgements_2=judgements_df.copy()

#Create a list of every tenor as string
strList=list()
for tenor in judgements_2['Tenor']:
    tenor = ''.join(tenor)
    strList.append(tenor)
    
#overwrite the tenor list with the tenor strings
judgements_2["Tenor"]=strList


#check if abgewiesen in Tenor = 0 else 1
intList=list()
for tenor in judgements_2['Tenor']:
     if "angenommen" in tenor:
       intList.append(1)
     elif "abgewiesen" in tenor:
         intList.append(2)
     elif "zurückgewiesen" in tenor:
        intList.append(3)
     elif "zurückgenommen" in tenor:
        intList.append(4)
     elif "aufgehoben" in tenor:
        intList.append(5)
     else:
       intList.append(0)
#hinzufügen der werte ob abgewiesen in Abgewiesen
judgements_2["CheckTwo"]=intList

