import datetime
import re
import requests
from t4c_api import T4CApi
import pandas as pd
from dotenv import dotenv_values

config = dotenv_values(".env")
token=config['token']
licencekey=config['licencekey']


filename = 'data.csv'
host = config['host']
api = T4CApi(token, licencekey)


animals = {}
sires = {}


def endpoint(url):
    return host + url




def transfer_animal():
    url = host + "/api/cowcard/transfer/save"
    data = '{"AnimalId":,"TransferDate":"2023-01-15T13:53:31.000Z","TransferRemarks":"","ReasonType":2,"ReasonID":0,"AnimalLifeNumber":"","HerdId":0,"GroupId":0,"KeepAnimal":true,"OldHerdId":0,"NewHerdId":0,"ContactId":0,"UserNumber":20962}'
    response = requests.post(url, headers=headers, data=data)
    print(response.text)


def import_animal(cows):
    '''
    send cows to server by 10 pieces in one request
    :param cows: list of dicts
    return ok or error
    '''

    for i in range(0, len(cows), 5):
        data = {"CommonFields": {"GroupId": 819, "HerdId": 3, "TransferReasonType": "2", "TransferReasonId": "",
                                 "TransferDate": "", "TransferContactId": ""}, 'SpecificFields': []}
        for cow in cows[i:i + 5]:
            data['SpecificFields'].append({"UserNumber": cow[1],
                                           "ResponderNumber": "",
                                           "LifeNumber": "EE 00" + cow[1],
                                           "IgnoreLifeNumberFormat": True,
                                           'BirthDate': cow[4],
                                           "LactationNumber": "",
                                           "CalvingDate": None,
                                           "InseminationDate": None})
        api.post_batch_animal(data)


'''
{"CommonFields":{"GroupId":0,"HerdId":3,"TransferReasonType":"2","TransferReasonId":"",
"TransferDate":"","TransferContactId":""},"SpecificFields":[
{"UserNumber":1111,"ResponderNumber":"","LifeNumber":"EE 1111","IgnoreLifeNumberFormat":true,
"BirthDate":"2023-01-17T00:00:00.000Z","LactationNumber":"","CalvingDate":null,"InseminationDate":null}]}
'''


def date_to_iso(date):
    # convert date to iso format
    try:
        return datetime.datetime.strptime(date, '%d.%m.%y').strftime('%Y-%m-%dT00:00:00.000Z')
    except ValueError:
        return ''


'''
def read_csv(file):
    # import csv file and return list of dicts
    data = []
    #usernames = [animal['usernumber'] for animal in animals]
    with open(file, 'r', encoding='utf8', newline='') as f:
        lines = f.readlines()
        for num, line in enumerate(lines[1:]):
            # skip " in line
            # get date by mask 10.01.21 and convert to iso format in line
            line = re.sub(r'(\d{2}\.\d{2}\.\d{2})', lambda m: date_to_iso(m.group(1)), line)
            line = line.replace('"', '')
            line = line.replace(' ', ' ')
            line = line.replace('\r\n', '')
            line = line.split(',')
            #chek if line[1] is already exist in animals dict
            if line[12] in usernames:
                print(line[12])
            data.append(line)

    return data
'''


def get_sireid_by_sirecode(SireCode):
    for sire in sires:
        if sire['SireCode'] == SireCode:
            return sire['Id']
    return None


def get_animalid_by_usernumber(usernumber):
    for animal in animals:
        if animal['usernumber'] == int(usernumber):
            return animal['id']
    return None


def import_insemination(inseminations):
    return None


'''
    {"SpecificFields":[{"Id":0,"AnimalId":6053,"SireId":null,"Remarks":"",
    "CheckPregnant":true}],"CommonFields":{"ContactId":1,
    "Date":"2023-01-18T00:00:00.000Z","GroupId":null,"InseminationTypeId":1}}
    
    [{"AnimalId":6053,"Date":"2023-01-21T00:00:00.000Z",
    "InseminationTypeId":1,"SireId":742,"GroupId":0,
    "ContactId":39,"ChargeNumber":"","Remarks":"test","CheckPregnant":true}]
'''


def read_csv(file):
    # read csv file with pandas "Reg. nr.",Inv. nr.,"","Nimi",Sünd,"Sünnikaal","Söötpv","Isa","Ema",
    # "EI","Viim. seem.","Nr.","Pull","Sugus","VP grupp","Tõug","PI","Kaalumine","Kaal","Iive","Ehitis","TK"
    df = pd.read_csv(file, sep=',', encoding='utf8')
    for index, row in df.iterrows():
        # chkeck if Viim. seem. is not empty
        if row['Viim. seem.'] != ' ':
            print(row['Viim. seem.'])
            print(row['Pull'])
            # check if Pull code is in sires
            if get_sireid_by_sirecode(row['Pull']) is None:
                api.save_sire({"Id": 0, "SireName": row['Pull'], "LifeNumber": "", "SireCode": row['Pull'],
                               "SireDescription": "Automatically imported from Vissuke", "Active": True,
                               "InFarm": False, "CheckLifeNumber": False, "AnimalNumber": ""}
                              )
            api.saveBatchInsemination([{"AnimalId": get_animalid_by_usernumber(row['Inv. nr.']),
                                        "Date": row['Viim. seem.'],
                                        "InseminationTypeId": 1,
                                        "SireId": get_sireid_by_sirecode(row['Pull']),
                                        "GroupId": 0,
                                        "ContactId": 39,
                                        "ChargeNumber": "",
                                        "Remarks": "Automatically imported from Vissuke",
                                        "CheckPregnant": True}])


if __name__ == "__main__":
    animals = api.get_animals('herdid=3')['Data']
    sires = api.get_sires()['Data']
    print(len(animals))
