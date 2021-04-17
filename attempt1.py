import bz2
import json
import re #regualr expressions
import csv
from langdetect import detect



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

    #loser case string
    return m_mod.lower()


def calculateCovidTweets(tweet,numCovid,numMaybeCovid):
    print(tweet)
    s = cleanATweet(tweet)
    print(s)
    

    #covid-19
    r1 = re.search(r'c+(\s)*o+(\s)*v+(\s)*i+(\s)*d+(\s)*-*_*(\s)*(19+)*', s)
    #corona virus
    r2 = re.search(r'c+(\s)*o+(\s)*r+(\s)*o+(\s)*n+(\s)*a+(\s)*(v+(\s)*i+(\s)*r+(\s)*u+(\s)*s)*',s)
    #epidemic
    r3 = re.search(r'e+(\s)*p+(\s)*i+(\s)*d+(\s)*e+(\s)*m+(\s)*i+(\s)*c+',s)
    #face mask
    r4 = re.search(r'f+(\s)*a+(\s)*c+(\s)*e+(\s)*m+(\s)*a+(\s)*s+(\s)*k+(\s)*(s+)*',s)


    # print(s)
    # print(s.upper())

    weight = 0

    #weight is in desending order
    if r1:
        # print('Match found case 1: ', r1.group())
        print('Match found case 1: ')
        weight += 1
    if r2:
        # print('Match found case 1: ', r1.group())
        print('Match found case 2: ')
        weight += 1
    if r3 or r4:
        # print('Match found case 1: ', r1.group())
        print('Match found case 3/4: ')
        weight += 0.5
    # else:
    #     print('No match')

    print("weight: " + str(weight))

    return weight



def modifyDate():
    s1 = "Mon Jan 20 07:29:00 +0000 2020"

def main ():

    numTotalTweets = 0

    with open(r'datasets\Twitter\20_big\20temp.csv', encoding='utf-8') as f:
    # with open(r'datasets\Twitter\20_big\20temp.csv','r', newline='',encoding='utf-8') as f:
        data_file = csv.reader(f,delimiter=',')
        numTotalTweets= len(list(data_file))
        print(numTotalTweets)
        # print(data_file)

        i = 0
        for row in data_file:
            i +=1
            if i <=3:
                print(', '.join(row))

    numCovidTweets = 0
    numMaybeCovidTweets = 0

    s1 = "does this sentence contain covid? or idk !! 123"
    s2 = "oh no, no match@"
    s3 = "once corona did that?? okay oops covid-19 and epidemic"
    # calculateCovidTweets(s1, numCovidTweets,numMaybeCovidTweets)
    # calculateCovidTweets(s2, numCovidTweets,numMaybeCovidTweets)
    # calculateCovidTweets(s3, numCovidTweets,numMaybeCovidTweets)




if __name__=="__main__":

    main()
