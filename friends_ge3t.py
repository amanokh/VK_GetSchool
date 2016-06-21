# -*- coding: utf-8 -*-
import http.client, urllib
schools={}
sch_count={}
token=input('token:')                     #for getting a school info of private user, may skip
user_id=input('userid:')
print ("")
print ("Connecting to VK...")
data = {}
data['user_id']=user_id
data['fields']='city,schools'
data['access_token']=token
data['v']='5.42'
params = urllib.parse.urlencode(data)
conn = http.client.HTTPSConnection("api.vk.com")
conn.request("POST", "/method/friends.get", params)
response = conn.getresponse()
print (response.status, response.reason)
answer = response.read()
dic=eval(answer)            #transform json answer to dictionary

print ("Parsing users...")
pupils=int(dic['response']['count'])
for i in dic['response']['items']:
    try:
        for sc in i['schools']:         #for people with 2 or more schools in profile
            scid=sc['id']
            schools[scid]='%s, %s' % (sc['name'], sc['city'])       #adding a school info to 'schools' dictionary
            sch_count[scid]=sch_count.get(scid, 0)+1
    except KeyError:
        z=0
    except IndexError:
        z=0
sch_count=sorted(sch_count.items(), key=lambda x: x[1])     #sorting schools by amount of it's pupils-friends
k=-1
while k!=-4:            #top-3 results
    percent=round((sch_count[k][1]/pupils)*100, 2)
    print ('%s ---- %s' % (schools[sch_count[k][0]], percent), '%,', '%s of %s friends' % (sch_count[k][1], pupils))
    k-=1

conn.close()
