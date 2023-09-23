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
with open("out.html", "w") as f:
	print(sesh.getCalendarUrl(ExportParams.Duration.NEXT_WEEK, ExportParams.Events.ALL))
	f.write(str(sesh.getCalendarUrl(ExportParams.Duration.NEXT_WEEK, ExportParams.Events.ALL)))
