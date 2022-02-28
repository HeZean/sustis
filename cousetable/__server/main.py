import asyncio
from datetime import datetime, timedelta

from icalendar import Calendar, Event, vText
import pandas as pd
import pytz

from get_raw import get_raw

weeks_date = pd.read_csv('proc/meta.csv')
course_time = pd.read_csv('proc/time.csv')

cal = Calendar()


def add_event():
    event = Event()
    event.add('summary', course_name)
    event['location'] = vText(location)

    year = int(row[1]['mon_date'].split('-')[0])
    mo = int(row[1]['mon_date'].split('-')[1])
    day = int(row[1]['mon_date'].split('-')[2])
    st_hr = int(course_time['SH'][int(course_no) - 1])
    st_min = int(course_time['SM'][int(course_no) - 1])
    end_hr = int(course_time['EH'][int(course_no) - 1])
    end_min = int(course_time['EM'][int(course_no) - 1])
    weekday = timedelta(days=(int(course_day) - 1))
    event.add('dtstart', (datetime(year, mo, day, st_hr, st_min, 0,
                                   tzinfo=pytz.timezone('Asia/Shanghai')) + weekday))
    event.add('dtend', (datetime(year, mo, day, end_hr, end_min, 0,
                                 tzinfo=pytz.timezone('Asia/Shanghai')) + weekday))

    cal.add_component(event)


if __name__ == '__main__':
    try:
        asyncio.run(get_raw())
    except Exception as e:
        print(e)

    week_list = []
    lang = input('Use Chinese or English? [c/e]  ').upper()
    
    course_list = pd.read_csv('proc/table.csv')
    for _, course in course_list.iterrows():
        course_name = course['name_cn' if lang == 'C' else 'name_en']
        course_day = course['weekday']
        course_no = course['class_of_day']
        location = course['location']

        course_week_type = course['norm_odd_even']
        for row in weeks_date.iterrows():
            if course_week_type == 0:
                add_event()
            elif course_week_type == 1 and (row[1]['week'] % 2 == 1):
                add_event()
            elif course_week_type == 2 and (row[1]['week'] % 2 == 0):
                add_event()

    with open('schedule.ics', 'wb') as f:
        f.write(cal.to_ical())

    print('All done, have fun!')
