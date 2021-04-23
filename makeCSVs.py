import os
import bz2
import json
import csv
import codecs
import re #regular expressions
import glob
import random
from langdetect import detect

'''
name: 
    cleanATweet
parameter: 
    string of a tweet
description:
    removes non alphbetical characters

returns:
    string where words are seperated by spaces, and all characters are lower case
'''

def cleanATweet(message):
    #do some regex stuff here
    
    # print("original tweet vs cleaned tweet:")
    # print(message) 

    #remove the '.' and ',' from the tweet
    # tweet_mod = message.translate({ord(i): None for i in ',.'})
   
    # word_list = message.split()
    # print()
    #list of words
    temp = re.findall(r"\w+",message)
    m_mod = ""

    for w in temp:
        m_mod += w + " "

    # print(m_mod)

    #lower case string
    return m_mod.lower()

def modifyDate(raw_date):
    s1 = raw_date
    temp_list = s1.split()

    temp_date = ""

    if(temp_list[1] == "Jan"):
        temp_date = temp_list[2] + "/01/2020"
    elif(temp_list[1] == "Feb"):
        temp_date = temp_list[2] + "/02/2020"
    else:
        temp_date = temp_list[2] + "/03/2020"

    return temp_date
'''
name: 
    addToOutputFile
parameter: 
    string of a tweet
description:
    removes non alphbetical characters

returns:

'''

def addToOutputFile(s_file, output_file,attributes_keep,wr):

    # print("Attempting to open: " + filename)
    # source_file = bz2.open(filename,"r") #r for text files, rb for non text files

    # count = 0
    # countHasCountry = 0

    # meta_attributes_keep = ["created_at","id","text"] #keep these from tweet

    fieldnames = attributes_keep

    langErrors = 0

    #'a': append file contents
    with open(output_file, 'a', newline='',encoding='utf-8') as csvfile:
                
        # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        # writer.writeheader() #writes the headers to the CSV file

        #https://docs.python.org/3/library/datetime.html

        for i, line in enumerate(s_file):
            # count += 1

            #check every 5th line (keep 20%)
            if (i%8 !=1):
                continue

            #line is kinda json, make this into json object (dictionary)
            tweet = json.loads(line)

            dtemp = {}

            # if count <= 200: #remove this later 
                # if count <= 100: #remove this later

            try:
                #igonore non english tweets, don't add to CSV
                lang = detect(tweet['text'])
                # print(lang)
                if(lang != "en"):
                    continue
            except:
                #language detect has issues with URLs, numbers, emojis, etc.
                langErrors += 1
                # print(tweet['text'])

            #ignore deleted tweets
            if("delete" in tweet): 
                # print(str(count) + " DELETE")
                continue

            #get random 0.0001% of english tweets
            # 10.0 % : 0.10
            #  0.10% : 0.001 
            # r = random.random() #generate random number between 0 and 1
            # if r < 0.00001:
            #     continue


            clean_tweet = cleanATweet(tweet['text'])
            covid_num = calculateCovidInTweet(clean_tweet)
            symptom_num = calculateSymptomsInTweet(clean_tweet)

            if covid_num ==0.0 and symptom_num==0.0:
                continue

            for att in attributes_keep:

                if str(att) == "created_at":
                    dtemp[att] = modifyDate(tweet[att])

                elif str(att) == "text":
                    dtemp[att] = clean_tweet

                elif str(att) == "covid_weight":
                    try:
                        dtemp[att] = covid_num
                    except:
                        dtemp[att] = ""

                elif str(att) == "symptom_weight":
                    try:
                        dtemp[att] = symptom_num
                    except:
                        dtemp[att] = ""

                else:
                    dtemp[att] = tweet[att]


            # print(dtemp)

            
            wr.writerow(dtemp)

    # print("number of tweets w/ countries: " + str(countHasCountry))
    # print("number of tweets total: " + str(count))
    # print("Language detection Errors: " + str(langErrors))
    return 0


def calculateCovidInTweet(tweet):
    # print(tweet)
    s = cleanATweet(tweet)

    # main word list 

    #covid-19
    r1 = re.search(r'c+(\s)*o+(\s)*v+(\s)*i+(\s)*d+(\s)*-*_*(\s)*(19+)*', s)
    #corona virus
    r2 = re.search(r'c+(\s)*o+(\s)*r+(\s)*o+(\s)*n+(\s)*a+(\s)*(v+(\s)*i+(\s)*r+(\s)*u+(\s)*s)*',s)
    #sars-cov-2
    r3 = re.search(r's+(\s)*a+(\s)*r+(\s)*s+(\s)*-*_*(\s)*c+(\s)*o+(\s)*v+(\s)*-*_*(\s)*2',s)
    #social distanci//ng
    r4 = re.search(r's+(\s)*o+(\s)*c+(\s)*i+(\s)*a+(\s)*l+(\s)*d+(\s)*i+(\s)*s+(\s)*t+(\s)*a+(\s)*n+(\s)*c+(\s)*i',s)
    #face covering
    r5 = re.search(r'f+(\s)*a+(\s)*c+(\s)*e+(\s)*c+(\s)*o+(\s)*v+(\s)*e+(\s)*r+(\s)*i+(\s)*n+(\s)*g',s)
    #physical distanci//ng
    r6 = re.search(r'p+(\s)*h+(\s)*y+(\s)*s+(\s)*i+(\s)*c+(\s)*a+(\s)*l+(\s)*d+(\s)*i+(\s)*s+(\s)*t+(\s)*a+(\s)*n+(\s)*c+(\s)*i+(\s)*n+(\s)*g',s)
    #epidemic
    r7 = re.search(r'e+(\s)*p+(\s)*i+(\s)*d+(\s)*e+(\s)*m+(\s)*i+(\s)*c',s)
    #face mask
    r8 = re.search(r'f+(\s)*a+(\s)*c+(\s)*e+(\s)*m+(\s)*a+(\s)*s+(\s)*k',s)
    #pandemic
    r9 = re.search(r'p+(\s)*a+(\s)*n+(\s)*d+(\s)*e+(\s)*m+(\s)*i+(\s)*c',s)
    #surgical mask
    r10 = re.search(r's+(\s)*u+(\s)*r+(\s)*g+(\s)*i+(\s)*c+(\s)*a+(\s)*l+(\s)*m+(\s)*a+(\s)*s+(\s)*k',s)
    #quarantine
    r11 = re.search(r'q+(\s)*u+(\s)*a+(\s)*r+(\s)*a+(\s)*n+(\s)*t+(\s)*i+(\s)*n',s)
    #lockdown
    r12 = re.search(r'l+(\s)*o+(\s)*c+(\s)*k+(\s)*e+(\s)*d+(\s)*o+(\s)*w+(\s)*n',s)
    #outbreak
    r13 = re.search(r'o+(\s)*u+(\s)*t+(\s)*b+(\s)*r+(\s)*e+(\s)*a+(\s)*k',s)
    #personal protective equipm//ent
    r14 = re.search(r'p+(\s)*e+(\s)*r+(\s)*s+(\s)*o+(\s)*n+(\s)*a+(\s)*l+(\s)*p+(\s)*r+(\s)*o+(\s)*t+(\s)*e+(\s)*c+(\s)*t+(\s)*i+(\s)*v+(\s)*e+(\s)*e+(\s)*q+(\s)*u+(\s)*i+(\s)*p+(\s)*m',s)
    #respirator
    r15 = re.search(r'r+(\s)*e+(\s)*s+(\s)*p+(\s)*i+(\s)*r+(\s)*a+(\s)*t+(\s)*o+(\s)*r',s)
    #vaccine
    r16 = re.search(r'v+(\s)*a+(\s)*c+(\s)*c+(\s)*i+(\s)*n+(\s)*e',s)
    #virus
    r17 = re.search(r'v+(\s)*i+(\s)*r+(\s)*u+(\s)*s',s)

    weight = 0

    #weight is in desending order
    
    word_weights = [ [r1,1], [r2,1], [r3,1], [r4,0.8], [r5,0.6], 
                    [r6,0.6], [r7,0.5], [r8,0.4], [r9,0.4], [r10,0.3],
                    [r11,0.3], [r12,0.25], [r13,0.2], [r14,0.2], [r15,0.2],
                    [r16,0.1], [r17,0.1] ]

    for val in word_weights:

        if val[0]:
            weight += float(val[1])


    return weight

def calculateSymptomsInTweet(tweet):
    # print(tweet)
    s = cleanATweet(tweet)
    
    #------------symptom word list---------
    #fever
    s1 = re.search(r'f+(\s)*e+(\s)*v+(\s)*e+(\s)*r',s)
    #cough
    s2 = re.search(r'c+(\s)*o+(\s)*u+(\s)*g+(\s)*h',s)
    #fatigue
    s3 = re.search(r'f+(\s)*a+(\s)*t+(\s)*i+(\s)*g+(\s)*u+(\s)*e',s)
    #tired
    s4 = re.search(r't+(\s)*i+(\s)*r+(\s)*e+(\s)*d',s)
    #mucus
    s5 = re.search(r'm+(\s)*u+(\s)*c+(\s)*u+(\s)*s',s)
    #shortness of breath
    s6 = re.search(r's+(\s)*h+(\s)*o+(\s)*r+(\s)*t+(\s)*n+(\s)*e+(\s)*s+(\s)*s+(\s)*o+(\s)*f+(\s)*b+(\s)*r+(\s)*e+(\s)*a+(\s)*t+(\s)*h',s)
    #hard to breath
    s7 = re.search(r'h+(\s)*a+(\s)*r+(\s)*d+(\s)*t+(\s)*o+(\s)*b+(\s)*r+(\s)*e+(\s)*a+(\s)*t+(\s)*h',s)
    #out of breath
    s8 = re.search(r'o+(\s)*u+(\s)*t+(\s)*o+(\s)*f+(\s)*b+(\s)*r+(\s)*e+(\s)*a+(\s)*t+(\s)*h',s)
    #dyspnea
    s9 = re.search(r'd+(\s)*y+(\s)*s+(\s)*p+(\s)*n+(\s)*e+(\s)*a',s)
    #mayalgia
    s10 = re.search(r'm+(\s)*a+(\s)*y+(\s)*a+(\s)*l+(\s)*g+(\s)*i+(\s)*a',s)
    #muscle pain
    s11 = re.search(r'm+(\s)*u+(\s)*s+(\s)*c+(\s)*l+(\s)*e+(\s)*p+(\s)*a+(\s)*i+(\s)*n',s)
    #sore throat
    s12 = re.search(r's+(\s)*o+(\s)*r+(\s)*e+(\s)*t+(\s)*h+(\s)*r+(\s)*o+(\s)*a+(\s)*t',s)
    #head ache
    s13 = re.search(r'h+(\s)*e+(\s)*a+(\s)*d+(\s)*a+(\s)*c+(\s)*h+(\s)*e',s)

    # print(s)
    # print(s.upper())

    symptom_weight = 0

    #weight is in desending order

    s_word_weights = [ [s1,0.879], [s2,0.667], [s3,0.381], [s4,0.381], [s5,0.334], 
                    [s6,0.186], [s7,0.186], [s8,0.186], [s9,0.186], [s10,0.148],
                    [s11,0.148], [s12,0.139], [s13,0.136] ]

    for val in s_word_weights:

        if val[0]:
            symptom_weight += float(val[1])

    return symptom_weight

def main ():

    # beginning_path = r"datasets\Twitter\20\00\\" #notice the double slash charcter is needed

    # output_f = r'datasets\Twitter\20_big\20csv.txt' #output file
    output_f = r'datasets\Twitter\clean\01_jan_clean\day13.csv' #output file

    folder_contents = os.listdir(r"datasets\Twitter\20\00\\")

    #list containing the names of the files and subdirectories in the directory given by the path argument:
    # print(folder_contents) #https://realpython.com/working-with-files-in-python/

    # w+ : Opens a file writing and reading. Overwrites the existing file if the file exists. 
    #   If the file does not exist, creates a new file for reading and writing.
    output_file = codecs.open(output_f,'w+','utf-8') 

    output_file.close()

    count = 0

    meta_attr = ["created_at","id","text","covid_weight","symptom_weight"] #keep these from tweet

    with open(output_f, 'a', newline='',encoding='utf-8') as csvfile:
                
        writer = csv.DictWriter(csvfile, fieldnames=meta_attr)
    
        writer.writeheader() #writes the headers to the CSV file

        #go through folder and open all bz2 files
        # for x in folder_contents:
        for x in glob.glob(r"datasets\Twitter\raw\01_jan_raw\13\*\*"):
        # for x in glob.glob(r"datasets\Twitter\raw\*\*\*\*"):
            # filename = beginning_path + str(x)
            filename = x

            print(filename)
            source_file = bz2.open(filename,"r") #r for text files, rb for non text files

            # addToOutputFile(filename,output_f)
            addToOutputFile(source_file,output_f,meta_attr,writer) # @@@@@

            source_file.close()

            # if count == 2: #remove 'if' to read entire folder
            #     break
            # count = count +1

    output_file.close()



    
if __name__=="__main__":

    main()

# recursive open bz2 files