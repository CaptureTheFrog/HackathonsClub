#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import json
import datetime

months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sept", "oct", "nov", "dec"]

if __name__ == '__main__':
	h = []
	for i in range(2021, 2025):
		r = requests.get(f"https://www.hackathons.org.uk/events/{i}")
		soup = BeautifulSoup(r.text, 'html.parser')
		divs = soup.select('div#upcoming-events > div.grid > div')
		for div in divs:
			img = None
			img_tag = div.select_one('img[srcSet]')
			if img_tag and img_tag.get('src') is not None and img_tag.get('src') != 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTkyMCIgaGVpZ2h0PSI5NzUiIHZpZXdCb3g9IjAgMCAxOTIwIDk3NSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjE5MjAiIGhlaWdodD0iOTc1IiBmaWxsPSIjRTkxRTYzIi8+CjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNMCAyMjMuMTIzTDgwIDI0MS4wMjVDMTYwIDI1OC45MjcgMzIwIDI5NC43MzEgNDgwIDMzMC41MzRDNjQwIDM2Ni4zMzggODAwIDQwMi4xNDIgOTYwIDM2Ni4zMzhDMTEyMCAzMzAuNTM0IDEyODAgMjIzLjEyMyAxNDQwIDE4Ny4zMkMxNjAwIDE1MS41MTYgMTc2MCAxODcuMzIgMTg0MCAyMDUuMjIxTDE5MjAgMjIzLjEyM1Y5NzVIMTg0MEMxNzYwIDk3NSAxNjAwIDk3NSAxNDQwIDk3NUMxMjgwIDk3NSAxMTIwIDk3NSA5NjAgOTc1QzgwMCA5NzUgNjQwIDk3NSA0ODAgOTc1QzMyMCA5NzUgMTYwIDk3NSA4MCA5NzVIMFYyMjMuMTIzWiIgZmlsbD0iI0QxMTQ1NSIvPgo8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTE5MjAgNjAyLjc3OEwxODEyLjggNTUzLjE0OEMxNzA3LjIgNTAzLjUxOSAxNDkyLjggNDA0LjI1OSAxMjgwIDQxNi42NjdDMTA2Ny4yIDQyOS4wNzQgODUyLjggNTUzLjE0OCA2NDAgNTUzLjE0OEM0MjcuMiA1NTMuMTQ4IDIxMi44IDQyOS4wNzQgMTA3LjIgMzY3LjAzN0wwIDMwNVY5NzVIMTA3LjJDMjEyLjggOTc1IDQyNy4yIDk3NSA2NDAgOTc1Qzg1Mi44IDk3NSAxMDY3LjIgOTc1IDEyODAgOTc1QzE0OTIuOCA5NzUgMTcwNy4yIDk3NSAxODEyLjggOTc1SDE5MjBWNjAyLjc3OFoiIGZpbGw9IiNBMzEwNDIiLz4KPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0wIDc0NC45NDdINjRDMTI4IDc0NC45NDcgMjU2IDc0NC45NDcgMzg0IDc1My45NDdDNTEyIDc2My45NDcgNjQwIDc4Mi45NDcgNzY4IDczNC45NDdDODk2IDY4Ni45NDcgMTAyNCA1NzEuOTQ3IDExNTIgNTEzLjk0N0MxMjgwIDQ1Ni45NDcgMTQwOCA0NTYuOTQ3IDE1MzYgNTA0Ljk0N0MxNjY0IDU1Mi45NDcgMTc5MiA2NDguOTQ3IDE4NTYgNjk2Ljk0N0wxOTIwIDc0NC45NDdWOTc0Ljk0N0gxODU2QzE3OTIgOTc0Ljk0NyAxNjY0IDk3NC45NDcgMTUzNiA5NzQuOTQ3QzE0MDggOTc0Ljk0NyAxMjgwIDk3NC45NDcgMTE1MiA5NzQuOTQ3QzEwMjQgOTc0Ljk0NyA4OTYgOTc0Ljk0NyA3NjggOTc0Ljk0N0M2NDAgOTc0Ljk0NyA1MTIgOTc0Ljk0NyAzODQgOTc0Ljk0N0MyNTYgOTc0Ljk0NyAxMjggOTc0Ljk0NyA2NCA5NzQuOTQ3SDBWNzQ0Ljk0N1oiIGZpbGw9IiM3NDBCMkYiLz4KPC9zdmc+Cg==':
			    img = img_tag.get('src')
			name_span = div.select_one('span.text-xl')
			name = name_span.get_text(strip=True) if name_span else None
			date_span = div.select('p > span')[0]
			date = date_span.get_text(strip=True)
			location = div.select('p > span')[1].get_text(strip=True) if len(div.select('p > span')) == 2 else None
			digital_status = div.select_one('span.bg-green') is not None
			website_url = div.select_one('a')['href'] if div.select_one('a') else None
			
			start = date.split("-")[0]
			end = date.split("-")[1]
			
			nh = {
				'name' : name,
				'url' : website_url,
				'image' : img,
				'start_date' : datetime.datetime(i, months.index(start.split(" ")[1].lower()) + 1, int(start.split(" ")[0])).isoformat(),
				'location_name' : location,
				'attendees' : None,
				'end_date' : datetime.datetime(i, months.index(end.split(" ")[1].lower()) + 1, int(end.split(" ")[0])).isoformat(),
				'digital_only' : digital_status
			}
			h.append(nh)
	f = open('../events_hackuk.org.json' , 'w')
	f.write(json.dumps(h))

