import urllib2
import json

def make_hist(alliance):
    raw = urllib2.urlopen('http://eve-kill.net/epic/victimAlliance:'+alliance+'/startDate:08-01-12.12.0.0/endDate:08-31-12.12.0.0/mask:1048576').read()
    parsed = json.loads(raw)
    rawitems = []
    # pull the items out from the individual killmails and put them all in one list
    for elem in parsed:
        if(elem['items'] != None):
            rawitems.extend(elem['items']['dropped'])
            rawitems.extend(elem['items']['destroyed'])
    fitteditems = []
    # drop all items that were not modules fitted to the ship at time of kill
    for item in rawitems:
        if int(item['itemSlot']) <= 3:
            fitteditems.append(item)

    # pull out unique names and count them to obtain a histogram
    names = [x['typeName'] for x in fitteditems]
    uniques = set(names)
    hist = [[name,names.count(name)] for name in uniques]
    return hist

def merge(h1, h2):
    orig = set([x[0] for x in h1])
    ret = h1
    temp = []
    for item in h2:
        if item[0] in orig:
            ret[find(item[0],h1)][1] = ret[find(item[0],h1)][1] + item[1]
        else:
            temp.append(item)
    ret.extend(temp)
    return ret

def find(item,li):
    for elem in li:
        if(elem[0] == item):
            return li.index(elem)

if __name__ == '__main__':
    losses = make_hist('Of+Sound+Mind')
    losses = merge(losses,make_hist('Yulai+Federation'))
    losses = merge(losses,make_hist('Curatores+Veritas+Alliance'))
    losses = merge(losses,make_hist('Sev3rance'))

    f = open('lossmails.csv','w')
    for item in losses:
        f.write(item[0]+','+str(item[1])+'\n')
    
    
        
