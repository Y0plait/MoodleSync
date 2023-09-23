#!/usr/bin/python3

import MoodleSyncMain
from MoodleSyncExtras import ExportParams

sesh = MoodleSyncMain.MoodleSession(username="a.moulin",
				    password="yjrM94o3wI",
				    baseUrl="https://cr-moodle.leschartreux.com")
sesh.login()
with open("out.html", "w") as f:
	print(sesh.getCalendarUrl(ExportParams.Duration.NEXT_WEEK, ExportParams.Events.ALL))
	f.write(str(sesh.getCalendarUrl(ExportParams.Duration.NEXT_WEEK, ExportParams.Events.ALL)))
