import os
import bz2
import json
import csv
import codecs
import re #regular expressions
import glob
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

    count = 0
    countHasCountry = 0

    # meta_attributes_keep = ["created_at","id","text"] #keep these from tweet

    fieldnames = attributes_keep

    langErrors = 0

    #'a': append file contents
    with open(output_file, 'a', newline='',encoding='utf-8') as csvfile:
                
        # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        # writer.writeheader() #writes the headers to the CSV file

        #https://docs.python.org/3/library/datetime.html

        for line in s_file:
            count += 1

            #line is kinda json, make this into json object (dictionary)
            tweet = json.loads(line)

            dtemp = {}

            # if count <= 200: #remove this later 
                # if count <= 100: #remove this later

            #ignore deleted tweets
            if("delete" in tweet): 
                # print(str(count) + " DELETE")
                continue

            # print(tweet['user']['screen_name'])

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

            # dtemp = {}

            for att in attributes_keep:

                if str(att) == "text":
                    dtemp[att] = cleanATweet(tweet[att])
                elif str(att) == "location":
                        # dtemp[att] = tweet['user'][att]
                    try:
                        dtemp[att] = cleanATweet(tweet['user']['location'])
                    
                    except:
                        dtemp[att] = ""

                elif str(att) == "country":
                    try:
                        dtemp[att] = tweet["place"]["country_code"]
                        countHasCountry +=1
                    except:
                        dtemp[att] = ""

                elif str(att) == "covid_weight":
                    try:
                        dtemp[att] = calculateCovidInTweet(dtemp["text"])
                    except:
                        dtemp[att] = ""

                else:
                    dtemp[att] = tweet[att]

                

                

            # print(dtemp)

            
            wr.writerow(dtemp)

    print("number of tweets w/ countries: " + str(countHasCountry))
    print("number of tweets total: " + str(count))
    # print("Language detection Errors: " + str(langErrors))
    return 0


def calculateCovidInTweet(tweet):
    # print(tweet)
    s = cleanATweet(tweet)
    # print(s)
    

    #covid-19
    r1 = re.search(r'c+(\s)*o+(\s)*v+(\s)*i+(\s)*d+(\s)*-*_*(\s)*(19+)*', s)
    #corona virus
    r2 = re.search(r'c+(\s)*o+(\s)*r+(\s)*o+(\s)*n+(\s)*a+(\s)*(v+(\s)*i+(\s)*r+(\s)*u+(\s)*s)*',s)
    #epidemic
    r3 = re.search(r'e+(\s)*p+(\s)*i+(\s)*d+(\s)*e+(\s)*m+(\s)*i+(\s)*c+',s)
    #face mask
    r4 = re.search(r'f+(\s)*a+(\s)*c+(\s)*e+(\s)*m+(\s)*a+(\s)*s+(\s)*k+(\s)*(s+)*',s)

    r100 = re.search(r'y+(\s)*o+(\s)*u',s)
    # print(s)
    # print(s.upper())

    weight = 0

    #weight is in desending order
    if r1:
        # print('Match found case 1: ', r1.group())
        # print('Match found case 1: ')
        weight += 1
    if r2:
        # print('Match found case 1: ', r1.group())
        # print('Match found case 2: ')
        weight += 1
    if r3 or r4:
        # print('Match found case 1: ', r1.group())
        # print('Match found case 3/4: ')
        weight += 0.5
    if r100:
        # print('Match found case 1: ', r1.group())
        # print('Match found case 3/4: ')
        weight += 0.25
    # else:
    #     print('No match')

    # print("weight: " + str(weight))

    return weight


def main ():

    beginning_path = r"datasets\Twitter\20\00\\" #notice the double slash charcter is needed

    # output_f = r'datasets\Twitter\20_big\20csv.txt' #output file
    output_f = r'datasets\Twitter\20_big\20temp.csv' #output file

    folder_contents = os.listdir(r"datasets\Twitter\20\00\\")

    #list containing the names of the files and subdirectories in the directory given by the path argument:
    # print(folder_contents) #https://realpython.com/working-with-files-in-python/

    # w+ : Opens a file writing and reading. Overwrites the existing file if the file exists. 
    # If the file does not exist, creates a new file for reading and writing.
    output_file = codecs.open(output_f,'w+','utf-8') 

    output_file.close()

    #append next file contents
    # output_file = codecs.open(output_f,'a','utf-8') 

    count = 0

    meta_attr = ["created_at","id","text","location","country","covid_weight"] #keep these from tweet

    with open(output_f, 'a', newline='',encoding='utf-8') as csvfile:
                
        writer = csv.DictWriter(csvfile, fieldnames=meta_attr)
    
        writer.writeheader() #writes the headers to the CSV file

        #go through folder and open all bz2 files
        # for x in folder_contents:
        for x in glob.glob(r"datasets\Twitter\20\00\*"):
        # for x in glob.glob(r"datasets\Twitter\20\*\*"):
            # filename = beginning_path + str(x)
            filename = x

            # print(filename)
            source_file = bz2.open(filename,"r") #r for text files, rb for non text files

            # addToOutputFile(filename,output_f)
            addToOutputFile(source_file,output_f,meta_attr,writer) # @@@@@

            source_file.close()

            if count == 2: #remove 'if' to read entire folder
                break
            count = count +1

    output_file.close()

    #glob
    # for name in glob.glob(r"datasets\Twitter\20\*\*"):
    #     print(name)



    
if __name__=="__main__":

    main()

# recursive open bz2 files