# import urllib2
from urllib.request import urlopen

def get_list_ko(line):
    ## gets all pathway ids and their reactions from kegg
    try:
        pwid = line.split('\t')[0]
        pwname = line.split('\t')[1]
    except:
        print("Error getting list of KOs")
        return ["None"], "None"

    pwid = pwid[8:]
    ko = 'ko' + pwid
    url = str("http://rest.kegg.jp/link/ko/map" + pwid)
    try:
        data = urlopen(url, timeout=20).read()
    except ValueError:
        print("Error retrieving pathway IDs")
        pass
    # data = data.strip('\'')

    data = data.decode("utf-8") 
    data = data.split('\n')
    ko_in_path = []
    for row in data[:-1]:
        ko_in_path.append(row[-6:])

    return ko_in_path, pwname