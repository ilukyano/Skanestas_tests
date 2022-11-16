import random
import json
import os,re,datetime,statistics,time

initDDL="DDL.json"
initPATH=os.path.dirname(__file__)
#print(initPATH)
initAPF=os.path.join(initPATH, initDDL) #abs path file
#print(initAPF)

def gendata():
    with open(initAPF) as jdata: # opening ddl.json
        jdata=json.load(fp=jdata) #load json
        #print(jdata)
        jnew={} # create new major json
        bidlist=[] # create new bid list
        asklist=[] # create new ask list
        for i in jdata:
            if re.search("\d", i): #if tblname contains digit set var multiply by ten
                substr=i[-2:] # get substr from val where contains digits
                dig=float(substr) # do digit
                inthigh=dig*10 # set high edge for rand
                rnd = random.randint(1,inthigh)
                jnew[i]=rnd
                cntfieldname=i[:3] # get float field names
                if cntfieldname=='bid':
                    #print(cntfieldname)
                    bidlist.append(rnd)
                if cntfieldname=='ask':
                    #print(cntfieldname)
                    asklist.append(rnd)
                #print(inthigh)
                #print(jnew)
            else:
                if jdata[i]=='unix timestamp':
                       nowDate = datetime.datetime.now()
                       unix_timestamp = datetime.datetime.timestamp(nowDate)*1000
                       jnew[i]=unix_timestamp
                if jdata[i]=='json':
                    jnew[i]={}
        bidavg=statistics.mean(bidlist) # calc avg stats
        askavg=statistics.mean(asklist) # same as above
        jnew['stats']['bidavg']=bidavg # add avg stats
        jnew['stats']['askavg']=askavg # same as above
        return jnew

while True:
    i=gendata()
    print(i)
    time.sleep(1/1000)

       # print(i)
       # print(jdata[i])
        
#t='020'
#print(int(t))
        




