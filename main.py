import datetime
import time

import requests
from t4c_api import T4CApi
import pandas as pd
from dotenv import dotenv_values

config = dotenv_values(".env")
token=config['token']
licencekey=config['licencekey']
host = config['host']
filename = 'data.csv'
api = T4CApi(token, licencekey)


animals = {}
sires = {}
headers = {'Authorization': token, 'Content-Type': 'application/json',
           'licensekey': licencekey}



def import_animal(cows):
    """
    send cows to server by 10 pieces in one request
    :param cows: list of dicts
    return ok or error
    """

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



def date_to_iso(date):
    # convert date to iso format
    try:
        return datetime.datetime.strptime(date, '%d.%m.%y').strftime('%Y-%m-%dT00:00:00.000Z')
    except ValueError:
        return ''



def get_sireid_by_sirecode(sirecode):
    for sire in sires_in_db:
        if sire['SireCode'] == str(sirecode):
            return sire['Id']
    return None


def get_animalid_by_usernumber(usernumber):
    for animal in animals_in_db:
        if animal['usernumber'] == int(usernumber):
            return animal['id']
    raise Exception('Animal not found')


def import_siers(siers):
    for sier in siers:
        if sier['SireCode'] not in sires_in_db:
            api.save_sire(sier)


if __name__ == "__main__":
    animals_in_db = api.get_animals('herdid=3')['Data']
    sires_in_db = api.get_sires()['Data']
    print(sires_in_db)
    df = pd.read_csv(filename, sep=',', encoding='utf-8')
    # get all rows if 'Pull' have value exept ' ' and not repeat
    #df = df.drop_duplicates(subset=['Pull'])
    print(df[df['Pull'].str.len() > 4]['Pull'].count())
    for index, row in df.iterrows():
        if row['Pull'] != ' ' and len(row['Pull']) > 4:
            print(api.getInseminationHistoryData(get_animalid_by_usernumber(int(row['Inv. nr.']))))

    #cunt rows with 'Pull' that have len(row['Pull']) > 4
    #



