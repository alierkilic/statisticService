from flask import Flask, Response, request, render_template
import msgpack
from heapq import nlargest
from collections import defaultdict
from datetime import datetime
import os
from functools import reduce
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# database code
class Event(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    event_name = db.Column(db.String(20), nullable=False)
    first_data = db.Column(db.String(20), nullable=False)
    second_data = db.Column(db.String(20), nullable=False)

db.create_all()
db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == "POST":
        # write data to database
        deserialized_chunk = msgpack.unpackb(request.data)
        for data in deserialized_chunk:
            if data[1]=='signup':
                user = Event(time=int(data[0]), event_name=data[1], first_data=data[2], second_data='')
            else:
                user = Event(time=int(data[0]), event_name=data[1], first_data=data[2], second_data=data[3])
            db.session.add(user)
            db.session.commit()

        return "OK"

    else:
        all_events = Event.query.all()
        # 15 minutes in nanoseconds = 900000000000
        answers = get_statistics(all_events, 10, 900000000000)
        # data for plotting graph
        data_to_plot = answers[0]
        days_to_plot = range(1, len(data_to_plot) + 1)

        top_week_list = answers[1]

        average_session_time = answers[2]

    return render_template('page.html', value=average_session_time, lenn=len(top_week_list), len=len(top_week_list[0]), week_lists=top_week_list, max=550, labels=days_to_plot, values=data_to_plot)

def daily_user_plot(data_list):
    # Algorithm for daily active user graph
    # holds number of unique active users for each day
    number_of_daily_active_users = []
    # one day in nanoseconds
    one_day = 86400000000000
    # holds unique active users for day
    active_users_for_day = set([])

    if not data_list:
        return [0]
    # initialize start time in the beginning
    start_time = data_list[0].time
    # updates time to UTC+3
    nanosec = int(start_time) + (3600000000000 * 3)
    dt = datetime.utcfromtimestamp(nanosec // 1000000000)
    hour = dt.strftime('%H')
    minute = dt.strftime('%M')
    second = dt.strftime('%S')
    start_time = nanosec - (
            (3600000000000 * int(hour)) + (60000000000 * int(minute)) + (1000000000 * int(second)))



    # row variable is a list that represents a row in csv
    for row in data_list:

        # if user is active in that day add first_data to set
        if (int(row.time) < start_time + one_day):
            if row.event_name == 'follow':
                active_users_for_day.add(row.second_data)
            else:
                active_users_for_day.add(row.first_data)

        else:
            # update start time to next day
            start_time = start_time + one_day
            # add unique users of that day to the list which holds active users for each day
            number_of_daily_active_users.append(len(active_users_for_day))
            # prepare set for a new day
            active_users_for_day.clear()
    # in the end, if there are users left in the set add them to number_of_daily_active_users
    if (len(active_users_for_day) > 0):
        number_of_daily_active_users.append(len(active_users_for_day))
        active_users_for_day.clear()

    return number_of_daily_active_users
# end of algo for daily user graph

def get_weeks_top_N(data_list, N):
    # holds top N most viewed users for every week
    top_week_list = []

    # helps getting user id from the splash id
    splash_dict = {}

    # holds number of views for users
    view_counter = {}

    # one week in nanoseconds
    one_week = 604800000000000

    if not data_list:
        return []
    if N<1:
        return []
    # initialize start time in the beginning
    start_time = data_list[0].time
    # updates time to UTC+3
    nanosec = int(start_time) + (3600000000000 * 3)
    dt = datetime.utcfromtimestamp(nanosec // 1000000000)
    hour = dt.strftime('%H')
    minute = dt.strftime('%M')
    second = dt.strftime('%S')
    start_time = nanosec - (
            (3600000000000 * int(hour)) + (60000000000 * int(minute)) + (1000000000 * int(second)))

    for row in data_list:

        # get user ids from splash ids to calculate views for that week
        if (int(row.time) < start_time + one_week):
            if row.event_name == 'viorama':
                splash_dict[row.second_data] = row.first_data
            if row.event_name == 'view':
                viewed_first_data = splash_dict.get(row.second_data)
                # increment number of views for that user
                if viewed_first_data in view_counter:
                    view_counter[viewed_first_data] += 1
                else:
                    view_counter[viewed_first_data] = 1

        # go to next week
        else:
            start_time = start_time + one_week
            # gets N largest values in dictionary using nlargest
            res = nlargest(N, view_counter, key=view_counter.get)
            # adds that week's top 10 to general top 10 list
            top_week_list.append(res)
            # clears view counts
            view_counter = {}

    # in the end add top 10 of the last week
    if (len(view_counter) > 0):
        res = nlargest(N, view_counter, key=view_counter.get)
        top_week_list.append(res)
        view_counter = {}

    return top_week_list
    # end of top N of the week algo

# start of average user session algo
def get_avg_user_session(data_list, minute_in_ns):
    # dictionary with lists, holds time list for each first_data
    session_counter = defaultdict(list)
    # holds session time for each user session
    max_session = []

    # add time to the time list of the user in session_counter
    for row in data_list:
        if row.event_name == 'follow':
            session_counter[row.second_data].append(row.time)
        else:
            session_counter[row.first_data].append(row.time)

    for key in session_counter:
        next = 1
        prev = 0
        # holds total session time
        max = 0
        # get time list of that user
        session_list = session_counter[key]
        # no session in this case
        if len(session_list) < 2:
            None
        else:
            for time in session_list:
                # get difference and check if it exceeds 15 minutes
                difference = int(session_list[next]) - int(session_list[prev])
                # increment session time if the next activity is within 15 minutes
                if difference < minute_in_ns:
                    max += difference
                else:
                    # if next activity is not within 15 mins, finish session and append session time to session time list
                    max_session.append(max)
                    max = 0
                next += 1
                prev += 1
                # in the end add session times in the list
                if len(session_list) <= next:
                    if max > 0:
                        max_session.append(max)
                    break

    if not max_session:
        return "0"
    average_session_time = reduce(lambda a, b: a + b, max_session) / len(max_session)
    return str(average_session_time)

# algorithm for getting all statistics
def get_statistics(data_list, N, minute_in_ns):
    # holds number of unique active users for each day
    number_of_daily_active_users = []
    # one day in nanoseconds
    one_day = 86400000000000
    # holds unique active users for day
    active_users_for_day = set([])

    # holds top N most viewed users for every week
    top_week_list = []
    # helps getting user id from the splash id
    splash_dict = {}
    # holds number of views for users
    view_counter = {}
    # one week in nanoseconds
    one_week = 604800000000000

    # dictionary with lists, holds time list for each first_data
    session_counter = defaultdict(list)
    # holds session time for each user session
    max_session = []

    if not data_list:
        return [[0], [], 0]

    # initialize start time in the beginning
    start_time = data_list[0].time
    # updates time to UTC+3
    nanosec = int(start_time) + (3600000000000 * 3)
    dt = datetime.utcfromtimestamp(nanosec // 1000000000)
    hour = dt.strftime('%H')
    minute = dt.strftime('%M')
    second = dt.strftime('%S')
    start_time = nanosec - (
            (3600000000000 * int(hour)) + (60000000000 * int(minute)) + (1000000000 * int(second)))


    day_checker = start_time
    week_checker = start_time


    # row variable is a list that represents a row in csv
    for row in data_list:


        if (int(row.time) < day_checker + one_day):
            if row.event_name == 'follow':
                active_users_for_day.add(row.second_data)
            else:
                active_users_for_day.add(row.first_data)

        else:
            # update start time to next day
            day_checker = day_checker + one_day
            # add unique users of that day to the list which holds active users for each day
            number_of_daily_active_users.append(len(active_users_for_day))
            # prepare set for a new day
            active_users_for_day.clear()
        # in the end, if there are users left in the set add them to number_of_daily_active_users

        # get user ids from splash ids to calculate views for that week
        if (int(row.time) < week_checker + one_week):
            if row.event_name == 'viorama':
                splash_dict[row.second_data] = row.first_data
            if row.event_name == 'view':
                viewed_first_data = splash_dict.get(row.second_data)
                # increment number of views for that user
                if viewed_first_data in view_counter:
                    view_counter[viewed_first_data] += 1
                else:
                    view_counter[viewed_first_data] = 1

        # go to next week
        else:
            week_checker = week_checker + one_week
            # gets N largest values in dictionary using nlargest
            res = nlargest(N, view_counter, key=view_counter.get)
            # adds that week's top 10 to general top 10 list
            top_week_list.append(res)
            # clears view counts
            view_counter = {}

        if row.event_name == 'follow':
            session_counter[row.second_data].append(row.time)
        else:
            session_counter[row.first_data].append(row.time)

        # in the end add top 10 of the last week
    if (len(view_counter) > 0):
        res = nlargest(N, view_counter, key=view_counter.get)
        top_week_list.append(res)
        view_counter = {}

    if (len(active_users_for_day) > 0):
        number_of_daily_active_users.append(len(active_users_for_day))
        active_users_for_day.clear()

    for key in session_counter:
        next = 1
        prev = 0
        # holds total session time
        max = 0
        # get time list of that user
        session_list = session_counter[key]
        # no session in this case
        if len(session_list) < 2:
            None
        else:
            for time in session_list:
                # get difference and check if it exceeds 15 minutes
                difference = int(session_list[next]) - int(session_list[prev])
                # increment session time if the next activity is within 15 minutes
                if difference < minute_in_ns:
                    max += difference
                else:
                    # if next activity is not within 15 mins, finish session and append session time to session time list
                    max_session.append(max)
                    max = 0
                next += 1
                prev += 1
                # in the end add session times in the list
                if len(session_list) <= next:
                    if max > 0:
                        max_session.append(max)
                    break

    average_session_time = reduce(lambda a, b: a + b, max_session) / len(max_session)

    return [number_of_daily_active_users, top_week_list, str(average_session_time)]

if __name__ == '__main__':
    app.run(debug=True)