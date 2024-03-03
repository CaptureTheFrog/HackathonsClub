#!/usr/bin/python3

import requests
import yaml
import re
import datetime
import json

months = [
'january',
'february',
'march',
'april',
'may',
'june',
'july',
'august',
'september',
'october',
'november',
'december'
]

if __name__ == '__main__':
	h = []
	y = yaml.safe_load(requests.get('https://raw.githubusercontent.com/CaptureTheFrog/wiki/master/events.yml').content.decode("utf-8"))
	for season in y['extra']['hackathon_seasons']:
		year = int(season['name'].split(" ")[-1])
		for hackathon in season['hackathons']:
			print(hackathon['name'])
			dates = hackathon['when'].split("-")
			start_day = int(re.sub('\D', '', hackathon['when'].split("-")[0].split(" ")[0]))
			end_month = int(months.index(hackathon['when'].replace(str(year), '').strip().split("-")[-1].split(" ")[-1].lower())) + 1
			end_day = int(re.sub('\D', '', hackathon['when'].split("-")[1].split(" ")[0]) if "-" in hackathon['when'] else start_day)
			start_month = (int(months.index(hackathon['when'].split("-")[0].split(" ")[-1].lower())) + 1) if hackathon['when'].split("-")[0].split(" ")[-1].lower() in months else end_month
			digital = hackathon.get('digital') or False

			if hackathon.get('location'):
				location_name = hackathon.get('location')
			elif digital:
				location_name = "Online"
			else:
				location_name = None

			nh = {
				'name': hackathon['name'],
				'url': hackathon.get('website') or None,
				'start_date': datetime.datetime(year, start_month, start_day).isoformat(),
				'location_name': location_name,
				'attendees': (hackathon['attendees'] if hackathon['attendees'] != 'TBC' else None),
				'end_date': datetime.datetime(year, end_month, end_day).isoformat(),
				'digital_only': digital
			}

			h.append(nh)
	f = open('../events_hack.athons.uk.json' , 'w')
	f.write(json.dumps(h))
	
		
