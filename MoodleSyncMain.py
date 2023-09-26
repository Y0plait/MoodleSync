#!/bin/python3
"""

Filename: main.py
Author: Anton Moulin
Date (last edited): 20/09/2023

Abstract:
    Simple moodle API that implements the basic moodle features. Among which the capacity of
    getting the calendar for the upcoming week, as well as the files.

"""

from MoodleSyncExtras import ExportParams
import requests as req
import logging
import json

"""
Cookie & login process:

When the login page (https://cr-moodle.leschartreux.com/login/index.php) is fetched, the server
sends a cookie back to the client (cookie name: MoodleSession). This cookie must be used for the
whole time using the api. 
After that the login page is sent to the client, the server waits for a POST request that contains
the cookie and the auth information (password & login). 

"""
logging.basicConfig(filename="./app.log", filemode="w", format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


class MoodleSession():
    """
    TODO
    """
    
    def __init__(self, username: str, password: str, baseUrl: str):
        self.username = username
        self.password = password

        #If the base url ends with a / remove it:
        if baseUrl[-1] != "/":
            self.baseUrl = baseUrl
        else:
            self.baseUrl = baseUrl[:len(baseUrl)-1]


    def login(self):
        # Login process:
        #   -> first get of the login page (self.baseUrl+/login/index.php)
        #   -> save the cookie 'MoodleSession' that will be used until the MoodleSession object is destroyed
        #   -> extract the login token hidden in an input tag with the class name 'logintoken'
        #   -> format the payload like that:
        #       {
        #           "anchor": "",
        #           "logintoken": firstGet.parsed.token,
        #           "username": self.username,
        #           "password": self.password
        #           ""
        #       }
        self.session=req.Session()
        firstGet=self.session.get(self.baseUrl+"/login/index.php")
        logging.debug(f"First get status code: {firstGet.status_code}")

        # Try to parse the cookie:
        try:
            self.connectionCookie=firstGet.cookies
        except KeyError:
            raise Exception("The MoodleSession cookie could not be found !")
            logging.critical("Cannot retrieve the MoodleSession cookie !")
        else:
            finderString='name="logintoken" value="'
            logintoken=firstGet.text[firstGet.text.find(finderString)+len(finderString):
                                     firstGet.text.find(finderString)+len(finderString)+32]
            logging.debug(f"Loggin token parsed: {logintoken}")
            
        payload = {
            "anchor": "",
            "logintoken": logintoken,
            "username": self.username,
            "password": self.password
        }
        logging.debug(f"Sending POST request to login url with data: {payload} and cookie: {self.connectionCookie}")

        loginPost=self.session.post(self.baseUrl+"/login/index.php", 
                          cookies=self.connectionCookie)
        #                 data=json.dumps(payload))
        # We don't need to send the cookies if we use the same session object used in the login process
        
        if loginPost.status_code != 200:
            logging.critical(f"Cannot login ! Connection refused: {loginPost.status_code}")
            raise ConnectionRefusedError("Cannot login ! Connection refused.")
        else:
            logging.info("Login successful!")
            myPage=self.session.get(self.baseUrl+"/my/", 
                           cookies=self.connectionCookie)
            self.sessKey = myPage.text[myPage.text.find('"sesskey":"')+11:
                                       myPage.text.find('"sesskey":"')+21]
            logging.debug(f"Sesskey found: {self.sessKey}")
                
        
    def getCalendarUrl(self, duration: ExportParams.Duration, events: ExportParams.Events) -> str:
        #To retrieve a calendar export url: make a POST request to the /calendat/export.php endpoint
        #with the following payload:
        payload = {
            "sesskey":self.sessKey,
            "_qf__core_calendar_export_form":1,
            "events[exportevents]":events,
            "period[timeperiod]":duration,
            "generateurl":"URL+du+calendrier"
        }

        logging.debug(f"Sending POST request to /calendar/export.php endpoint with payload: {payload}")

        # Posting the payload to the server
        calendarPost=self.session.post("https://cr-moodle.leschartreux.com/calendar/export.php", 
                                       cookies=self.connectionCookie)
        #                              data=json.dumps(payload))
        # We don't need to send the cookies if we use the same session object used in the login process

        # Parsing the url
        generatedUrl=calendarPost.text[calendarPost.text.find("URL du calendrier ")+21:
                                       calendarPost.text.find("URL du calendrier ")+100]

        return calendarPost.text

    def __del__(self):
        logging.info("Deleted MoodleSession object.")
        self.session.close()
