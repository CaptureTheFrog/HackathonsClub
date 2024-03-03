#!/usr/bin/python3

import json
import datetime

d1 = json.loads(open('../events_hackuk.org.json', 'r').read())
d2 = json.loads(open('../events_hack.athons.uk.json', 'r').read())

if __name__ == '__main__':
	q = list(e['name'] for e in d1)
	h = list(d1)
	for event in d1:
		for event2 in d2:
			if event2['name'].strip() in q:
				continue
			if event['start_date'] == event2['start_date'] and event['end_date'] == event2['end_date'] and event['name'].lower().replace(" ", "").strip() == event2['name'].lower().replace(" ", "").strip():
				continue
			q.append(event2['name'].strip())
			h.append(event2)
	f = open('../events.json' , 'w')
	f.write(json.dumps(h))
	

