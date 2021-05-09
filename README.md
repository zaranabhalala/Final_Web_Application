# Project Description
### Project features

1.  Create a login and registration process that includes email verification.  You can use a service like SendGrid to send email and you should look for a Flask Plugin to help.

2.  Create a calendar display and retrieve data out of Google Calendar.   Allow someone to add an even to their Google Calendar and display it on the page.  You can use the HTML full calendar plugin here (Links to an external site.) and you can probably make an iCal Feed from your Google calendar to feed into it, but you will need to cache the data locally in the database and update the data periodically between each request is made.  For example, if the calendar data has not been updated in 5 minutes, make a request to retrieve the data and update the database and then display that data in the fullCalendar page.
