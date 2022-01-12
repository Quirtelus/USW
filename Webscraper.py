

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
for x in numbers_list[0:2]:
	
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
            print(structured_data[0])
    #except:
        	#print('No findings.')
            #assign structured data to different datasets
            tenor = structured_data[0]
            tatbestand = structured_data[1]
            gruende = structured_data[2]
            final_list.append([link,tenor,tatbestand,gruende])
            print(link)
            print(final_list[0])
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
<<<<<<< Updated upstream
     if "abgewiesen" in tenor:
       intList.append(0)
     else:
       intList.append(1)
#hinzufügen der werte ob abgewiesen in Abgewiesen
judgements_2["Abgewiesen"]=intList
=======
     if "Die Klage wird abgewiesen" in tenor or "Kläger" and "Berufung" and "abgelehnt" in tenor or "Klägerin" and "Berufung" and "abgelehnt" in tenor:
       intList.append(1)
     elif "angenommen" in tenor or "Abschiebungsverbot festzustellen" in tenor or "Abschiebungsverbot" and "festzustellen" in tenor or "subsidiären Schutz zu gewähren" in tenor or "Bescheid des Bundesamtes" and "aufgehoben" in tenor or "Flüchtlingseigenschaft anzuerkennen" in tenor or "Abschiebungsverbot" and "festzustellen" in tenor or "§60 Abs. 5 AufenthG" and "vorliegen" in tenor or "subsidiären Schutz zuzuerkennen" in tenor or "Flüchtlingseigenschaft zuzuerkennen" in tenor:
       intList.append(2)
     else:
       intList.append(0)
judgements_2['abgewiesen']=intList
judgements_2.drop(judgements_2[judgements_2['abgewiesen'] == 0].index, inplace = True)
#hinzufügen der werte ob abgewiesen in Abgewiesen
judgements_2.reset_index(drop=True, inplace=True)
>>>>>>> Stashed changes



strList=list()
for tatbestand in judgements_2['Tatbestand']:
    tatbestand = ''.join(tatbestand)
    strList.append(tatbestand)

judgements_2["Tatbestand"]=strList

# build count vectorizer
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer(min_df = 5)
X = count_vect.fit_transform(judgements_2['Tatbestand'])
dtm = pandas.DataFrame(X.toarray())
dtm.columns = count_vect.get_feature_names()
data_dtm = dtm.copy()
data_dtm['#Abgewiesen#']=judgements_2["abgewiesen"]
dtm2 = dtm.copy()


from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
y=data_dtm['#Abgewiesen#']
x=data_dtm.drop('#Abgewiesen#',axis=1)
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,stratify=y)




# create train and test data
import random
sample = random.sample(range(len(data_dtm.index)), k=int(len(data_dtm.index)*0.8))
training = data_dtm.iloc[sample]
test = data_dtm.drop(sample)



# apply random forest classifier
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier()
forest.fit(x_train, y_train)
forest.score(x_test,y_test)

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Make predictions for the test set
y_pred_test = forest.predict(x_test)

# View the classification report for test data and predictions
print(classification_report(y_test, y_pred_test))
