import requests
import json
import datetime
import os

def apicheck():
    while True:
        try:
            api = open('api.txt', 'r')
            print('Found API file ', end='')
        except:
            api = open('api.txt', 'w')
            api = open('api.txt', 'r')
            print('Created API file ', end ='')
        api = api.read()
        if api == '':
            print('but it is empty. Please re-enter or get a new api key by doing /api in game.')
            api = open('api.txt', 'w')
            api.write(input('API Key: '))
            api.close()
        else:
            if requests.get("https://api.hypixel.net/skyblock/auctions_ended?key="+api).json()['success'] == True:
                print('with a working key.')
                return api
            else:
                print('but the key is invalid.')
                api = open('api.txt', 'w')
                api.write(input('API Key: '))
                api.close()

api = apicheck()
userName = input('IGN: ')

uuid = requests.get("https://api.mojang.com/users/profiles/minecraft/"+userName).json()
print('Found uuid for '+userName+' - '+uuid['id'])

guildID = requests.get("https://api.hypixel.net/findGuild?key="+api+"&byUuid="+uuid['id']).json()

guild = requests.get("https://api.hypixel.net/guild?key="+api+"&id="+str(guildID['guild'])).json()

guildMembers = []
gExp = []

def sortSecond(val):
    return val[1]

for i in range(len(guild['guild']['members'])):
    total = 0
    for x in range(6):
        f = list(guild['guild']['members'][i]['expHistory'].values())
        total += f[x]
    gExp.append(total)

for i in range(len(guild['guild']['members'])):
    names = requests.get('https://api.mojang.com/user/profiles/' + str(guild['guild']['members'][i]['uuid']) + '/names').json()
    guildMembers.append([names[len(names)-1]['name'], gExp[i]])
    print('Done - '+str(guildMembers[i][0]))

print('')

guildMembers.sort(key = sortSecond, reverse = True)

try:
    f = open(('Logs\\'+str(datetime.datetime.today().month)+'-'+str(datetime.datetime.today().day)+'-'+str(datetime.datetime.today().year)+'.txt'), 'w')
except:
    os.system('mkdir Logs')
    f = open(('Logs\\'+str(datetime.datetime.today().month)+'-'+str(datetime.datetime.today().day)+'-'+str(datetime.datetime.today().year)+'.txt'), 'w')

for i in range(len(guildMembers)):
    print(str(i+1) + ': '+guildMembers[i][0]+': '+str(guildMembers[i][1]))
    f.write(str(i+1) + ': '+guildMembers[i][0]+': '+str(guildMembers[i][1])+'\n')

f.close()

while True:
    pass
    
