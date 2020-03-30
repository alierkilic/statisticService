import unittest
import server

data_list = []

class Event:
    def __init__(self, time, event_name, first_data, second_data):
        self.time = time
        self.event_name = event_name
        self.first_data = first_data
        self.second_data = second_data



class TestUser(unittest.TestCase):

    global data_list
    def test_daily_user(self):
        # test empty list
        data_list.clear()
        self.assertEqual(server.daily_user_plot(data_list), [0])
        #Cumartesi, 8 Ağustos 2015 06:08:09.214 GMT+03:00 DST
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='5577006791947779410', second_data=''))
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='1241687973565112848', second_data=''))
        data_list.append(Event(time=int(1439003289214921956), event_name='follow', first_data='5577006791947779410',
                               second_data='1241687973565112848'))
        data_list.append(Event(time=int(1439003289214921956), event_name='viorama', first_data='5577006791947779410',
                               second_data='2547829344760061335'))
        self.assertEqual(server.daily_user_plot(data_list), [2])

        data_list.clear()
        #Cuma, 7 Ağustos 2015 00:30:59 GMT+03:00 DST
        data_list.append(
            Event(time=int(1438896659000000000), event_name='signup', first_data='5527096741947779411', second_data=''))
        #Cumartesi, 8 Ağustos 2015 06:08:09.214 GMT+03:00 DST
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='5577006791947779410', second_data=''))
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='1241687973565112848', second_data=''))
        data_list.append(Event(time=int(1439003289214921956), event_name='follow', first_data='5577006791947779410',
                               second_data='1241687973565112848'))
        data_list.append(Event(time=int(1439003289214921956), event_name='viorama', first_data='5577006791947779410',
                               second_data='2547829344760061335'))
        self.assertEqual(server.daily_user_plot(data_list), [1,2])

        data_list.clear()
        #Perşembe, 6 Ağustos 2015 22:17:39 GMT+03:00 DST
        data_list.append(
            Event(time=int(1438888659000000000), event_name='signup', first_data='5527096741947779411', second_data=''))
        #Cumartesi, 8 Ağustos 2015 06:08:09.214 GMT+03:00 DST
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='5577006791947779410', second_data=''))
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='1241687973565112848', second_data=''))
        data_list.append(Event(time=int(1439003289214921956), event_name='follow', first_data='5577006791947779410',
                               second_data='1241687973565112848'))
        data_list.append(Event(time=int(1439003289214921956), event_name='viorama', first_data='5577006791947779410',
                               second_data='2547829344760061335'))
        self.assertEqual(server.daily_user_plot(data_list), [1, 0, 2])

    # tests weeks top N
    def test_top_N_week(self):
        data_list.clear()
        # test empty list
        self.assertEqual(server.get_weeks_top_N(data_list, 10), [])
        #Çarşamba, 29 Temmuz 2015 19:50:59 GMT+03:00 DST
        data_list.append(
            Event(time=int(1438188659000000000), event_name='signup', first_data='11111111111111111', second_data=''))
        data_list.append(
            Event(time=int(1438188659000000000), event_name='signup', first_data='22222222222222222', second_data=''))
        #Çarşamba, 29 Temmuz 2015 19:51:09 GMT+03:00 DST
        data_list.append(Event(time=int(1438188669000000000), event_name='follow', first_data='11111111111111111',
                               second_data='22222222222222222'))
        # Perşembe, 6 Ağustos 2015 22:17:39 GMT+03:00 DST
        data_list.append(
            Event(time=int(1438888659000000000), event_name='signup', first_data='5527096741947779411', second_data=''))
        # Cumartesi, 8 Ağustos 2015 06:08:09.214 GMT+03:00 DST
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='5577006791947779410', second_data=''))
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='1241687973565112848', second_data=''))
        data_list.append(Event(time=int(1439003289214921956), event_name='follow', first_data='5577006791947779410',
                               second_data='1241687973565112848'))
        data_list.append(Event(time=int(1439003289214921956), event_name='viorama', first_data='5577006791947779410',
                               second_data='2547829344760061335'))
        self.assertEqual(server.get_weeks_top_N(data_list, 1), [[]])

        data_list.clear()
        # Çarşamba, 29 Temmuz 2015 19:50:59 GMT+03:00 DST
        data_list.append(
            Event(time=int(1438188659000000000), event_name='signup', first_data='11111111111111111', second_data=''))
        data_list.append(
            Event(time=int(1438188659000000000), event_name='signup', first_data='22222222222222222', second_data=''))
        # Çarşamba, 29 Temmuz 2015 19:51:09 GMT+03:00 DST
        data_list.append(Event(time=int(1438188669000000000), event_name='follow', first_data='11111111111111111',
                               second_data='22222222222222222'))
        data_list.append(Event(time=int(1438188669000000000), event_name='viorama', first_data='11111111111111111',
                               second_data='23243432535'))
        data_list.append(Event(time=int(1438188669000000000), event_name='viorama', first_data='22222222222222222',
                               second_data='2324344565432535'))
        #Çarşamba, 29 Temmuz 2015 19:52:49 GMT+03:00 DST
        data_list.append(Event(time=int(1438188769000000000), event_name='view', first_data='11111111111111111',
                               second_data='2324344565432535'))
        data_list.append(Event(time=int(1438188769000000000), event_name='view', first_data='22222222222222222',
                               second_data='23243432535'))
        #Çarşamba, 29 Temmuz 2015 19:54:29 GMT+03:00 DST
        data_list.append(
            Event(time=int(1438188869000000000), event_name='signup', first_data='333333333333333', second_data=''))
        #Çarşamba, 29 Temmuz 2015 19:54:49 GMT+03:00 DST
        data_list.append(Event(time=int(1438188889000000000), event_name='view', first_data='333333333333333',
                               second_data='23243432535'))


        # Perşembe, 6 Ağustos 2015 22:17:39 GMT+03:00 DST
        data_list.append(
            Event(time=int(1438888659000000000), event_name='signup', first_data='5527096741947779411', second_data=''))
        # Cumartesi, 8 Ağustos 2015 06:08:09.214 GMT+03:00 DST
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='5577006791947779410', second_data=''))
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='1241687973565112848', second_data=''))
        data_list.append(Event(time=int(1439003289214921956), event_name='follow', first_data='5577006791947779410',
                               second_data='1241687973565112848'))
        data_list.append(Event(time=int(1439003289214921956), event_name='viorama', first_data='5577006791947779410',
                               second_data='2547829344760069'))
        data_list.append(Event(time=int(1439003289214921956), event_name='viorama', first_data='5527096741947779411',
                               second_data='1114343213432535'))
        data_list.append(Event(time=int(1439003289214921956), event_name='viorama', first_data='1241687973565112848',
                               second_data='1124332445654328'))
        #Pazartesi, 10 Ağustos 2015 16:54:49.214 GMT+03:00 DST
        data_list.append(Event(time=int(1439214889214921956), event_name='view', first_data='1241687973565112848',
                               second_data='1114343213432535'))
        data_list.append(Event(time=int(1439214889214921956), event_name='view', first_data='5577006791947779410',
                               second_data='1114343213432535'))
        data_list.append(Event(time=int(1439214889214921956), event_name='view', first_data='333333333333333',
                               second_data='1114343213432535'))
        self.assertEqual(server.get_weeks_top_N(data_list, 10), [['11111111111111111','22222222222222222'], ['5527096741947779411']])
        self.assertEqual(server.get_weeks_top_N(data_list, 1),
                         [['11111111111111111'], ['5527096741947779411']])


    def test_average_session(self):
        data_list.clear()
        self.assertEqual(server.get_avg_user_session(data_list, 900000000000), "0")
        data_list.clear()
        # Perşembe, 6 Ağustos 2015 22:17:39 GMT+03:00 DST
        data_list.append(
            Event(time=int(1438888659000000000), event_name='signup', first_data='5527096741947779411', second_data=''))
        data_list.append(
            Event(time=int(1438888659000000000), event_name='signup', first_data='5577006791947779410', second_data=''))
        #Perşembe, 6 Ağustos 2015 22:18:09 GMT+03:00 DST
        data_list.append(Event(time=int(1438888689000000000), event_name='viorama', first_data='5577006791947779410',
                               second_data='2547829344222061222'))
        # Perşembe, 6 Ağustos 2015 22:18:09 GMT+03:00 DST
        data_list.append(Event(time=int(1438888689000000000), event_name='viorama', first_data='5527096741947779411',
                               second_data='254783334222061335'))
        #Perşembe, 6 Ağustos 2015 22:19:49 GMT+03:00 DST
        data_list.append(Event(time=int(1438888789000000000), event_name='view', first_data='5527096741947779411',
                               second_data='2547829344222061222'))

        self.assertEqual(server.get_avg_user_session(data_list, 900000000000), "80000000000.0")
        self.assertEqual(server.get_avg_user_session(data_list, 60000000000), "30000000000.0")

    def test_get_statistics(self):
        data_list.clear()
        self.assertEqual(server.get_statistics(data_list, 10, 900000000000), [[0], [], 0])
        data_list.clear()
        # Çarşamba, 29 Temmuz 2015 19:50:59 GMT+03:00 DST
        data_list.append(
            Event(time=int(1438188659000000000), event_name='signup', first_data='11111111111111111', second_data=''))
        data_list.append(
            Event(time=int(1438188659000000000), event_name='signup', first_data='22222222222222222', second_data=''))
        # Çarşamba, 29 Temmuz 2015 19:51:09 GMT+03:00 DST
        data_list.append(Event(time=int(1438188669000000000), event_name='follow', first_data='11111111111111111',
                               second_data='22222222222222222'))
        data_list.append(Event(time=int(1438188669000000000), event_name='viorama', first_data='11111111111111111',
                               second_data='23243432535'))
        data_list.append(Event(time=int(1438188669000000000), event_name='viorama', first_data='22222222222222222',
                               second_data='2324344565432535'))
        # Çarşamba, 29 Temmuz 2015 19:52:49 GMT+03:00 DST
        data_list.append(Event(time=int(1438188769000000000), event_name='view', first_data='11111111111111111',
                               second_data='2324344565432535'))
        data_list.append(Event(time=int(1438188769000000000), event_name='view', first_data='22222222222222222',
                               second_data='23243432535'))
        # Çarşamba, 29 Temmuz 2015 19:54:29 GMT+03:00 DST
        data_list.append(
            Event(time=int(1438188869000000000), event_name='signup', first_data='333333333333333', second_data=''))
        # Çarşamba, 29 Temmuz 2015 19:54:49 GMT+03:00 DST
        data_list.append(Event(time=int(1438188889000000000), event_name='view', first_data='333333333333333',
                               second_data='23243432535'))

        # Perşembe, 6 Ağustos 2015 22:17:39 GMT+03:00 DST
        data_list.append(
            Event(time=int(1438888659000000000), event_name='signup', first_data='5527096741947779411', second_data=''))
        # Cumartesi, 8 Ağustos 2015 06:08:09.214 GMT+03:00 DST
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='5577006791947779410', second_data=''))
        data_list.append(
            Event(time=int(1439003289214921956), event_name='signup', first_data='1241687973565112848', second_data=''))
        data_list.append(Event(time=int(1439003289214921956), event_name='follow', first_data='5577006791947779410',
                               second_data='1241687973565112848'))
        data_list.append(Event(time=int(1439003289214921956), event_name='viorama', first_data='5577006791947779410',
                               second_data='2547829344760069'))
        data_list.append(Event(time=int(1439003289214921956), event_name='viorama', first_data='5527096741947779411',
                               second_data='1114343213432535'))
        data_list.append(Event(time=int(1439003289214921956), event_name='viorama', first_data='1241687973565112848',
                               second_data='1124332445654328'))
        # Pazartesi, 10 Ağustos 2015 16:54:49.214 GMT+03:00 DST
        data_list.append(Event(time=int(1439214889214921956), event_name='view', first_data='1241687973565112848',
                               second_data='1114343213432535'))
        data_list.append(Event(time=int(1439214889214921956), event_name='view', first_data='5577006791947779410',
                               second_data='1114343213432535'))
        data_list.append(Event(time=int(1439214889214921956), event_name='view', first_data='333333333333333',
                               second_data='1114343213432535'))
        self.assertEqual(server.get_statistics(data_list, 10, 900000000000),
                         [[3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [['11111111111111111', '22222222222222222'], ['5527096741947779411']],'40000000000.0'])

        self.assertEqual(server.get_statistics(data_list, 1, 60000000000),
                         [[3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [['11111111111111111'], ['5527096741947779411']], '6666666666.666667'])
if __name__ == '__main__':
    unittest.main()
