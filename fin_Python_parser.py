import re
import json
import datetime

failed_password = {}
reverse_mapping = {}

with open(r"E:\auth.log") as f:
   a = f.readlines() 

def data_json(date_object, user, ip, fp_rm):
    if fp_rm == 'fp': #for failed_password
        if user not in failed_password[date_object]:
            failed_password[date_object][user] = {}

        if "IPLIST" not in failed_password[date_object][user]:
            failed_password[date_object][user]["IPLIST"] = {}
            failed_password[date_object][user]["TOTAL"] = 0
            
        if ip in failed_password[date_object][user]["IPLIST"]:
            failed_password[date_object][user]["IPLIST"][ip] += 1
            failed_password[date_object][user]["TOTAL"] += 1
        
        else:
            failed_password[date_object][user]["IPLIST"][ip] = 1
            failed_password[date_object][user]["TOTAL"] += 1
 

    elif fp_rm == 'rm': #for reverse_mapping
        if user not in reverse_mapping[date_object]:
             reverse_mapping[date_object][user] = {}
             
        if "IPLIST" not in reverse_mapping[date_object][user]:
            reverse_mapping[date_object][user]["IPLIST"] = {}
            reverse_mapping[date_object][user]["TOTAL"] = 0
            
        if ip in reverse_mapping[date_object][user]["IPLIST"]:
            reverse_mapping[date_object][user]["IPLIST"][ip] += 1
            reverse_mapping[date_object][user]["TOTAL"] += 1
        
        else:
            reverse_mapping[date_object][user]["IPLIST"][ip] = 1
            reverse_mapping[date_object][user]["TOTAL"] += 1
         

def nvl(given_date,date_object):
    if given_date == "":
        return date_object
    return given_date

given_date= ""        
given_date= input('Enter the date in YYYY-MM-DD or leave it blank :') 
   
#print(given_date)
for i in a:
    j = i.split()
    date_string = j[1] +' '+ j[0]
    date_object = datetime.datetime.strptime("{0} 2018".format(date_string), "%d %b %Y").strftime("%Y-%m-%d")
    if date_object == nvl(given_date,date_object):
        if date_object not in failed_password :
            failed_password[date_object] = {}
        if date_object not in reverse_mapping:
            reverse_mapping[date_object] = {}
            
        ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', i)
        #print(ip)
        if j[5] == "Failed" and j[6]=="password" and ip != []:
            data_json(date_object, j[8], ip[0],'fp')
        elif j[5] == "reverse":
            user = j[10]
            data_json(date_object, user, ip[0],'rm')


#for deleting empty dictionaries
for val in failed_password:
    empty_keys = [k for k,v in failed_password[val].items() if not v]
    for k in empty_keys:
        del failed_password[val][k]

for val in reverse_mapping:
    empty_keys = [k for k,v in reverse_mapping[val].items() if not v]
    for k in empty_keys:
        del reverse_mapping[val][k]
#print(failed_password)

out_file = open("E:\my.json", "w")
json.dump(failed_password, out_file, indent=6)
out_file.close()