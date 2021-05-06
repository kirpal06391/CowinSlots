from datetime import date
from datetime import datetime
from datetime import timedelta  
import subprocess, json
from urllib import request, parse

age = 18
for_18 = []
today = date.today()
ts = datetime.now()
print(ts)

def getAvailableSlots(date):
    shell_proc = subprocess.Popen(['./getVaccineStatus.sh', date], stdout=subprocess.PIPE)
    data = shell_proc.stdout.read()
    try:
        json_data = json.loads(data)
    except:
        print("Response wasn't in JSON")
        data_post = parse.urlencode({"value1": "Vaccine Slot Alert"}).encode()
        # Replace Event with your IFTTT applet event & webhook_key with your webhook service key
        req = request.Request("https://maker.ifttt.com/trigger/{event}/with/key/{webhook_key}", data=data_post)
        resp = request.urlopen(req)
        exit()
    
    for center in json_data['centers']:
        for session in center['sessions']:
            if session['min_age_limit'] == age and session['available_capacity'] > 1:
                for_18.append(center)

for x in range(0,4):
    date=today + timedelta(days=x*7)
    date_fmted = date.strftime("%d-%m-%Y")
    getAvailableSlots(date_fmted)

alert_list = []
for center in for_18:
    capacity = 0
    for session in center['sessions']:
        if session['min_age_limit'] == age:
            capacity += session['available_capacity']
    center_dict = {"name": center['name'], "add": center['address'], "cap": capacity, "PIN": center['pincode']}
    if not any(d['name'] == center['name'] for d in alert_list):
        alert_list.append(center_dict)
sorted_alert_list = sorted(alert_list, key = lambda x: x['cap'], reverse=True)
post_obj = {}
for x in range(0,min(3, len(sorted_alert_list))):
    val = sorted_alert_list[x]['name']+"; "+sorted_alert_list[x]['add']+" | "+str(sorted_alert_list[x]['PIN'])+": "+str(sorted_alert_list[x]['cap'])
    post_obj.update({"value"+str(x+1): val})

if len(sorted_alert_list) > 0:
    data_post = parse.urlencode(post_obj).encode()
    # Replace Event with your IFTTT applet event & webhook_key with your webhook service key
    req = request.Request("https://maker.ifttt.com/trigger/{event}/with/key/{webhook_key}", data=data_post)
    resp = request.urlopen(req)
print(json.dumps(sorted_alert_list))
#print(post_obj)
#print(json.dumps(for_18))

""" JSON Format for Reference
{
            "address": "38 SREEDHAR ROY RD KOL-700039",
            "block_name": "Borough-VII",
            "center_id": 596773,
            "district_name": "Kolkata",
            "fee_type": "Free",
            "from": "09:00:00",
            "lat": 22,
            "long": 88,
            "name": "UPHC 66",
            "pincode": 700014,
            "sessions": [
                {
                    "available_capacity": 0,
                    "date": "11-05-2021",
                    "min_age_limit": 45,
                    "session_id": "f6023005-cf74-40ac-9695-09de15defb7c",
                    "slots": [
                        "09:00AM-11:00AM",
                        "11:00AM-01:00PM",
                        "01:00PM-03:00PM",
                        "03:00PM-04:00PM"
                    ],
                    "vaccine": "COVISHIELD"
                }
            ],
            "state_name": "West Bengal",
            "to": "16:00:00"
        }
"""
