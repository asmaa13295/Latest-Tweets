import json,requests,csv
import datetime

# change these values with your own one
bearer_token = ''
keyword = ''

#calculate date two weeks ago in utc time format
today = datetime.datetime.utcnow()
twoWeeks = datetime.timedelta(days = 14)
dateTwoWeeksAgo = (today - twoWeeks).strftime("%Y%m%d%H%M")

items = []
nextFrom = ''

# twitter end point url
url = 'https://api.twitter.com/1.1/tweets/search/30day/dev.json?query='+keyword+'&fromDate='+dateTwoWeeksAgo
result = requests.get(url, headers={'authorization': 'Bearer ' + bearer_token}).json()
items = result['results']
#request the data 9 times more as by default the max number of returned data is 100
if(len(items) < 1000 and len(result['next']) > 0):
    for i in range(9):
        url = 'https://api.twitter.com/1.1/tweets/search/30day/dev.json?query='+keyword+'&fromDate='+dateTwoWeeksAgo+'&next='+result['next']
        result = requests.get(url, headers={'authorization': 'Bearer ' + bearer_token}).json()
        items = items + result['results']

# rearrange data
def get_leaves(items, key=None):
    if isinstance(items, dict):
        leaves = {}
        for i in items.keys():
            leaves.update(get_leaves(items[i], i))
        return leaves
    elif isinstance(items, list):
        leaves = {}
        for i in items:
            leaves.update(get_leaves(i, key))
        return leaves
    else:
        return {key : items}

json_data = items

# parse all entries to get the complete fieldname list
fieldnames = set()

for entry in json_data:
    fieldnames.update(get_leaves(entry).keys())
#save data in csv file
with open('output.csv', 'w', newline='') as f_output:
    csv_output = csv.DictWriter(f_output, fieldnames=sorted(fieldnames))
    csv_output.writeheader()
    csv_output.writerows(get_leaves(entry) for entry in json_data)
