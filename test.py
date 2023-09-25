#!/usr/bin/python3

import MoodleSyncMain
from MoodleSyncExtras import ExportParams
import json

with open("ids.json", "r") as ids_file:
	ids = json.loads(ids_file.read())

sesh = MoodleSyncMain.MoodleSession(username=ids["username"],
				    password=ids["password"],
				    baseUrl="https://cr-moodle.leschartreux.com")
sesh.login()
calendarUrl=sesh.getCalendarUrl(ExportParams.Duration.NEXT_WEEK, ExportParams.Events.ALL)
print(calendarUrl)

with open("out.html", "w") as f:
	
	f.write(str(calendarUrl))
