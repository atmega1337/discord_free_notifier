import json
import os
from datetime import datetime

import discordsend
import get_epic
import get_steam
import get_ue


tokenfile="token.txt"
dbfile="data.json"

# создание файла
def readtoken(path):
    if os.path.isfile(path):
        file = open(path, 'r')
        webhooktoken = file.read()
        file.close()
        return webhooktoken
    else:
        print("Pls, create file {} and write webhook token on this file.".format(path))
        input()
        exit()

# создание файла
def createfile(path, data):
    with open(path, "w", encoding='utf-8') as file:
        file.write(data)
    file.close()

# Открытие листа
def openjson(path):
    file = open(path, "r", encoding='utf-8')
    data = json.load(file)
    file.close()
    return data

# Открытие листа
def openfile(path):
    #Открываем файл
    file = open(path, "r", encoding='utf-8')
    list = file.read().splitlines()
    # закрываем файл
    file.close()
    return list

# Открытие листа
def idelemetn(variable,array):
    """Поиск id элемента:
        variable - Что ищем

        array - В каком массиве

    Returns:
        id массива
    """
    for i in range(len(array)):
        if array[i]['game'] == variable:
            return i
    return



nowdata=datetime.toordinal(datetime.now())

webhooktoken=readtoken(tokenfile)

data = {
    'Steam': get_steam.get_free_steam_games(),
    'Epic': get_epic.get_free_epic_games(),
    'UE': get_ue.get_free_ue(),
}

# Create db - data.json
if not os.path.exists(dbfile):
    createfile(dbfile, json.dumps(data, sort_keys=False, indent=4))


filedata=openjson(dbfile)

# add new element to db and update timer test
for i in data: #platform 
    for x in data[i]:
        # Поиск по существующим элементам массива в filedata
        y= idelemetn(x['game'],filedata[i])
        # Если есть текузая позиция
        if not y == None:
            filedata[i][y]['test']=nowdata
        #если нету - добовляем
        else:
            filedata[i].append(x)
            newid=len(filedata[i])-1
            filedata[i][newid]['test']=nowdata
createfile(dbfile, json.dumps(filedata, sort_keys=False, indent=4))

# Send webhook
for i in filedata:
    for id in range(len(filedata[i])):
        if not 'discordsend' in filedata[i][id]:
            filedata[i][id]['discordsend']=False
        if not filedata[i][id]['discordsend']:
            if discordsend.discord_send(webhooktoken, i, filedata[i][id]["game"], filedata[i][id]["url"], filedata[i][id]["img"], filedata[i][id]["description"]):
                filedata[i][id]['discordsend']=True
                print( f'[{i}] {filedata[i][id]["game"]} send to discord')
        else:
            print( f'[{i}] {filedata[i][id]["game"]} there is discord')
createfile(dbfile, json.dumps(filedata, sort_keys=False, indent=4))

# Delete after 7 day
for i in filedata:
    for id in range(len(filedata[i])):
        datainfo=filedata[i][id]["test"]
        period = nowdata - datainfo
        if period > 7:
            print( f'[{i}] {filedata[i][id]["game"]} delete in db')
            filedata[i].pop(id)
            

createfile(dbfile, json.dumps(filedata, sort_keys=False, indent=4))
