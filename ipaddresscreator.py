from collections import defaultdict
import subprocess, sys, json, requests, os

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step
ip_addressLIST = []
cleanedLIST = []
values = []

def merge_dictionary(dictionary, merged):
    for key, value in dictionary.items():
        if isinstance(value, list):
            merged[key].extend(value)
        else:
            merged[key].append(value)
    return merged

def merge_dlist(*args):
    merged_dict = defaultdict(list)
    for dictionary in args:
        merged_dict = merge_dictionary(dictionary, merged_dict)
    return merged_dict


my_domain = input("type in the name of the domain you want to search: ")
print("getting tracert to " + my_domain)
newfilepath = "C:\Python34\\" + my_domain + "_file.txt"
with open(newfilepath, 'w') as outfile:
    subprocess.call(['tracert', '-d', my_domain], stdout = outfile)

for line in open(my_domain + "_file.txt"):
    separator = ' '
    line = line.split(separator)
    for value in line:
        values.append(value)

length = len(values)
for x in range(0,length):
    values[x] = values[x].strip()

[cleanedLIST.append(x) for x in values if x]

cleanedlength = len(cleanedLIST)

for i in range(0,cleanedlength):
    if cleanedLIST[i] == '*':
        cleanedLIST.insert( i+1 , 'ms')
        cleanedlength = cleanedlength+1
    if cleanedLIST[i] == 'Request':
        cleanedlength = cleanedlength-8
        break
    
for i in my_range(18, cleanedlength, 8):
    ip_addressLIST.append(cleanedLIST[i])

    
print("writing to " + "JSONdata_" + my_domain +".json")
baseurl = "http://ip-api.com/json/"
urlparameters = "?fields=country,regionName,city,lat,lon,org"
iplength = len(ip_addressLIST)
jsondictionary = defaultdict(list)
for i in range(2,iplength):
            JSONresponse = requests.get(baseurl + ip_addressLIST[i] + urlparameters)
            tempdict = json.loads(JSONresponse.text)
            if i == 2:
                jsondictionary = tempdict
            if i > 2:
                jsondictionary = merge_dlist(jsondictionary, tempdict)
                
                
                
with open("JSONdata_" + my_domain +".json", "w") as json_data:
            print(json.dumps(jsondictionary), file=json_data)
print("Done!")

    
    
    
    
    
    
    
    
    


