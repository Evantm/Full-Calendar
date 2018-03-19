import json
from datetime import datetime
import datetime as dt

master_dict = {}
rooms = {}
room_set = set()

days_of_week = {
    'monday':0,
    'tuesday':1,
    'wednesday':2,
    'thursday':3,
    'friday':4,
    'saturday':5,
    'sunday':6
    }

with open('201820.json','r') as file:
    master_dict = json.loads(file.read())


for subj in master_dict:
    for section in master_dict[subj]['data']:
        subj = section['subjectCourse']
        if(subj == 'COMP3610'): print(json.dumps(section,indent=4))
        if len(section['meetingsFaculty']) == 0: continue

        meeting_times = section['meetingsFaculty'][0]['meetingTime']

        #print(meeting_times)

        start_date = meeting_times['startDate']
        end_date = meeting_times['endDate']

        #print(days)
        #print(start_date,end_date)


        for key,vals in meeting_times.items():

            build = meeting_times['building']
            room = meeting_times['room']
            if vals == True and key != 'creditHourSession':
                
                start_time = meeting_times['beginTime']
                end_time = meeting_times['endTime']

                if None in [start_time,start_date,end_date,end_time]: continue

                start = datetime.strptime(start_date+start_time, "%m/%d/%Y%H%M")
                second = datetime.strptime(start_date+end_time, "%m/%d/%Y%H%M")
                end = datetime.strptime(end_date, "%m/%d/%Y")

                while start <= end:
                    start += dt.timedelta(days=1)
                    second += dt.timedelta(days=1)

                    if(start.weekday() == days_of_week[key]):
                        #print(subj,str(build)+" "+str(room),start.__format__("%m/%d/%YT%H:%M:00"),start_time,end_time)
                        room_code = str(build)+str(room)
                        event = {
                         'title': subj,
                         'start': start.__format__("%Y-%m-%dT%H:%M:00"),
                         'end': second.__format__("%Y-%m-%dT%H:%M:00")
                         }

                        room_list = rooms.get(room_code,[])
                        room_list.append(json.dumps(event))
                        rooms[room_code] = room_list
                        room_set.add(room_code)
                        #print(room_code,event)


#room_list = list(room_set)
#for room_ in room_list:
#    out = []
#    for room,classes in rooms.items():
#        if room_ == room:
#            for class_ in classes:
#                day_dict = json.loads(class_)
#                out.append(day_dict)
#    with open(f'C:\\Users\\etmac\\OneDrive\\Desktop\\Programming\\Full Calendar\\rooms\\{room_}.json','w') as file:
#        file.write( 'var class_ = ' +json.dumps(out,indent=4) + ';')
# We need to take data that looks like startDate: "startDate": "01/08/2018" and "endDate": "04/28/2018",
# With days being listen as Monday:True Tuesday:False etc
# 
# for meeting in meetinfaculty
#       take meeting time and day of the week and classroom and dates
#       iter through startdate to enddate one day at a time
#       if day in day of week then that class is on that date 
#  {
#          title: 'Meeting',
#          start: '2018-03-12T10:30:00',
#          end: '2018-03-12T12:30:00'
#        },
#
#
#

'''
"id": 89474,
                "isSectionLinked": false,
                "linkIdentifier": null,
                "maximumEnrollment": 40,
                "meetingsFaculty": [
                    {
                        "category": "01",
                        "class": "net.hedtech.banner.student.schedule.SectionSessionDecorator",
                        "courseReferenceNumber": "20108",
                        "faculty": [],
                        "meetingTime": {
                            "beginTime": "1000",
                            "building": "OM",
                            "buildingDescription": "Old Main Building",
                            "campus": "K",
                            "campusDescription": "Kamloops",
                            "category": "01",
                            "class": "net.hedtech.banner.general.overall.MeetingTimeDecorator",
                            "courseReferenceNumber": "20108",
                            "creditHourSession": 3.0,
                            "endDate": "04/28/2018",
                            "endTime": "1115",
                            "friday": true,
                            "hoursWeek": 2.5,
                            "meetingScheduleType": "LEC",
                            "monday": false,
                            "room": "2622",
                            "saturday": false,
                            "startDate": "01/08/2018",
                            "sunday": false,
                            "term": "201820",
                            "thursday": false,
                            "tuesday": false,
                            "wednesday": true
                        },
                        "term": "201820"
                    }
                ],
                "openSection": true,
                "partOfTerm": "1",
                "scheduleTypeDescription": "Lecture",
                "seatsAvailable": 1,
                "sequenceNumber": "01",
                "subject": "ACCT",
                "subjectCourse": "ACCT1000",
                "subjectDescription": "ACCT-Accounting",
                "term": "201820",
                "termDesc": "Winter 2018 (Jan-Apr)",
                "waitAvailable": 94,
                "waitCapacity": 100,
                "waitCount": 6
            },
            {
                "campusDescription": "Kamloops",
                "courseNumber": "1000",
                "courseReferenceNumber": "20109",
                "courseTitle": "Financial Accounting (3,0,0)",
                "creditHourHigh": null,
                "creditHourIndicator": null,
                "creditHourLow": 3,
                "creditHours": null,
                "crossList": null,
                "crossListAvailable": null,
                "crossListCapacity": null,
                "crossListCount": null,
                "enrollment": 39,
                "faculty": [
                    {
                        "bannerId": "T00357838",
                        "category": null,
                        "class": "net.hedtech.banner.student.faculty.FacultyResultDecorator",
                        "courseReferenceNumber": "20109",
                        "displayName": "Noskova, Jana",
                        "emailAddress": "jnoskova@tru.ca",
                        "primaryIndicator": true,
                        "term": "201820"
                    }
                ]


'''