from flask import Flask, Response, request, render_template
import msgpack
from heapq import nlargest
from collections import defaultdict
from datetime import datetime
import os
from functools import reduce

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    global global_data

    if request.method == "POST":
        # write data to global_data
        deserialized_chunk = msgpack.unpackb(request.data)
        global_data.extend(deserialized_chunk)

        return "OK"

    else:

        list_after_deserialization = global_data

        # 15 minutes in nanoseconds = 900000000000
        answers = get_statistics(list_after_deserialization, 10, 900000000000)
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
    start_time = 0
    # one day in nanoseconds
    one_day = 86400000000000
    # holds unique active users for day
    active_users_for_day = set([])

    # row variable is a list that represents a row in csv
    for row in data_list:
        # initialize start time in the beginning
        if start_time == 0:

            # updates time to UTC+3
            nanosec = int(row[0]) + (3600000000000 * 3)
            dt = datetime.utcfromtimestamp(nanosec // 1000000000)
            hour = dt.strftime('%H')
            minute = dt.strftime('%M')
            second = dt.strftime('%S')
            start_time = nanosec - (
                    (3600000000000 * int(hour)) + (60000000000 * int(minute)) + (1000000000 * int(second)))

        # if user is active in that day add user_id to set
        if (int(row[0]) < start_time + one_day):
            if row[1] == 'follow':
                active_users_for_day.add(row[3])
            else:
                active_users_for_day.add(row[2])

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

    start_time = 0
    # one week in nanoseconds
    one_week = 604800000000000

    for row in data_list:
        # initialize start time
        if start_time == 0:
            # updates time to UTC+3
            nanosec = int(row[0]) + (3600000000000 * 3)
            dt = datetime.utcfromtimestamp(nanosec // 1000000000)
            hour = dt.strftime('%H')
            minute = dt.strftime('%M')
            second = dt.strftime('%S')
            start_time = nanosec - (
                    (3600000000000 * int(hour)) + (60000000000 * int(minute)) + (1000000000 * int(second)))

        # get user ids from splash ids to calculate views for that week
        if (int(row[0]) < start_time + one_week):
            if row[1] == 'viorama':
                splash_dict[row[3]] = row[2]
            if row[1] == 'view':
                viewed_user_id = splash_dict.get(row[3])
                # increment number of views for that user
                if viewed_user_id in view_counter:
                    view_counter[viewed_user_id] += 1
                else:
                    view_counter[viewed_user_id] = 1

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
    # dictionary with lists, holds time list for each user_id
    session_counter = defaultdict(list)
    # holds session time for each user session
    max_session = []

    # add time to the time list of the user in session_counter
    for row in data_list:
        if row[1] == 'follow':
            session_counter[row[3]].append(row[0])
        else:
            session_counter[row[2]].append(row[0])

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

    # dictionary with lists, holds time list for each user_id
    session_counter = defaultdict(list)
    # holds session time for each user session
    max_session = []

    # initialize start time in the beginning
    start_time = data_list[0][0]
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


        if (int(row[0]) < day_checker + one_day):
            if row[1] == 'follow':
                active_users_for_day.add(row[3])
            else:
                active_users_for_day.add(row[2])

        else:
            # update start time to next day
            day_checker = day_checker + one_day
            # add unique users of that day to the list which holds active users for each day
            number_of_daily_active_users.append(len(active_users_for_day))
            # prepare set for a new day
            active_users_for_day.clear()
        # in the end, if there are users left in the set add them to number_of_daily_active_users

        # get user ids from splash ids to calculate views for that week
        if (int(row[0]) < week_checker + one_week):
            if row[1] == 'viorama':
                splash_dict[row[3]] = row[2]
            if row[1] == 'view':
                viewed_user_id = splash_dict.get(row[3])
                # increment number of views for that user
                if viewed_user_id in view_counter:
                    view_counter[viewed_user_id] += 1
                else:
                    view_counter[viewed_user_id] = 1

        # go to next week
        else:
            week_checker = week_checker + one_week
            # gets N largest values in dictionary using nlargest
            res = nlargest(N, view_counter, key=view_counter.get)
            # adds that week's top 10 to general top 10 list
            top_week_list.append(res)
            # clears view counts
            view_counter = {}

        if row[1] == 'follow':
            session_counter[row[3]].append(row[0])
        else:
            session_counter[row[2]].append(row[0])

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


# saves data given by client
global_data = []

if __name__ == '__main__':
    app.run(debug=True)