from pattern.web import Twitter
from pattern.en import sentiment
import matplotlib.pyplot as mpl

# set buzzwords (case insensitive)
words=[["Leo","DiCaprio","Leonardo"],["Christian","Bale"],["Matthew","McConaughey"],["Ejiofor","Chiwetel"],["Ellen","DeGeneres"],["Emma","Watson"],["Amy","Adams"]]
#words=[["12","Years","Slave"],["Wolf","Wall","Street"],["Gravity"],["American","Hustle"],["Nebraska"],["Dallas","Buyers","Club"],["Philomena"]]
words_friendly=['Leonardo DiCaprio','Christian Bale','Matther McConaughey','Ejiofor Chiwetel','Ellen DeGeneres','Emma Watson','Amy Adams']
#words_friendly=['12 Years of Slave','The Wolf of Wall Street','Gravity','American Hustle','Nebraska','Dallas Buyers Club','Philomena']

# initialize some lists
tweets=[]
freq=[]
sent=[]
avgf=[]
avgs=[]
time=[]

# acquire 100 evenly spaced clusters of up to 100 tweets each
T=Twitter(language="en")
for i in range(100):
   cluster=[]
   for tweet in T.search("#oscars".lower(),start=(440275000000000000-500000000000*i),count=1000,cached=False):
       cluster.append(tweet)
   tweets.append(cluster)

# create frequency and sentiment data for each buzzword over time
for buzz in words:
    data1=[]
    data2=[]
    for cluster in tweets:
        counter=0
        sen=0
        for tweet in cluster:
            for word in buzz:
                if word.lower() in tweet.text.lower():
                    counter=counter+1
                    sen+=sentiment(tweet.text)[0]
                    break
        if counter!=0: 
            sen=sen/counter
        data1.append(counter)
        data2.append(sen)
    freq.append(data1)
    sent.append(data2)

# match clusters to time
for n in range(len(tweets)):
    time.append(float(tweets[n][0].date[11:13])+float(tweets[n][0].date[14:16])/60+float(tweets[n][0].date[17:19])/360-12.0)

# smooth frequency data by finding averages over 5 clusters and graph it
for n in range(len(freq)):
    avgf.append([])
    avgf[n].append(float(sum(freq[n][0:1]))/2)
    avgf[n].append(float(sum(freq[n][0:2]))/3)
    for i in range(len(freq[n])-4):
        avgf[n].append(float(sum(freq[n][i:i+4]))/5)
    avgf[n].append(float(sum(freq[n][(len(freq[n])-2):len(freq[n])]))/3)
    avgf[n].append(float(sum(freq[n][(len(freq[n])-1):len(freq[n])]))/2)
    mpl.plot(time,avgf[n])

# format frequency graph
mpl.legend(words_friendly)
mpl.xlabel('Time (Mar 2, 2014, PM EST)')
mpl.ylabel('% of selected \'#oscars\' tweets mentioning topic')
mpl.title('Twitter topics of discussion during 2014 Oscars')
mpl.show()
mpl.figure()

# smooth sentiment data by finding averages over 7 clusters and graph it
for n in range(len(sent)):
    avgs.append([])
    avgs[n].append(float(sum(sent[n][0:1]))/2)
    avgs[n].append(float(sum(sent[n][0:2]))/3)
    avgs[n].append(float(sum(sent[n][0:3]))/4)
    for i in range(len(sent[n])-6):
        avgs[n].append(float(sum(sent[n][i:i+6]))/7)
    avgs[n].append(float(sum(sent[n][(len(sent[n])-3):len(sent[n])]))/4)
    avgs[n].append(float(sum(sent[n][(len(sent[n])-2):len(sent[n])]))/3)
    avgs[n].append(float(sum(sent[n][(len(sent[n])-1):len(sent[n])]))/2)
    mpl.plot(time,avgs[n])

# format sentiment graph
mpl.legend(words_friendly)
mpl.xlabel('Time (Mar 2, 2014, PM EST)')
mpl.ylabel('Average sentiment of selected \'#oscars\' tweets concerning topic')
mpl.title('Opinions on Twitter topics of discussion during 2014 Oscars')
mpl.show()