import httpx
import time

from codecs import replace_errors

import httpx
import time

class Train:
    def __init__(self, stationFrom, stationTo, date):
        self.time_in_way = None
        self.train_number = None
        self.time0 = None
        self.time1 = None
        self.code0 = None
        self.code1 = None
        client = httpx.Client()
        stationFrom = stationFrom.upper()
        stationTo = stationTo.upper()
        dateFrom = date.split()[0].split('-')
        dateFrom = str(dateFrom[2]) + "." + str(dateFrom[1]) + "." + str(dateFrom[0])
        timeT = date.split()[1][:5]
        self.stationFrom = stationFrom
        self.stationTo = stationTo
        self.date0 = dateFrom
        codeFrom = -1
        codeTo = -1
        stationsFrom = []
        urlFrom = "https://pass.rzd.ru/suggester?stationNamePart=" + stationFrom + "&lang=ru&compactMode=y"
        if client.get(urlFrom, follow_redirects=True).content !=None:
            stationsFrom = client.get(urlFrom, follow_redirects=True).json()
        if len(stationsFrom) > 1:
            for i in stationsFrom:
                s = i["n"]
                if (s.count('(') > 0):
                    i["n"] = s[:s.find("(") - 1]
                if i["n"] == stationFrom:
                    codeFrom = str(i["c"])
        if codeFrom == "-1":
            self.answer = "Ошибка в названии станции отправления"
        else: self.code0 = codeFrom
        urlTo = "https://pass.rzd.ru/suggester?stationNamePart=" + stationTo + "&lang=ru&compactMode=y"
        stationsTo = []
        if client.get(urlTo, follow_redirects=True) != None:
            stationsTo = client.get(urlTo, follow_redirects=True).json()
        if len(stationsTo) != 0:
            for i in stationsTo:
                s = i["n"]
                if (s.count('(') > 0):
                    i["n"] = s[:s.find("(") - 1]
                if i["n"] == stationTo:
                    codeTo = str(i["c"])
        if codeTo == "-1":
            self.answer =  "Ошибка в прибытии"
        else: self.code1 = codeTo
        if codeTo != -1 and codeFrom != -1:
            url = "https://pass.rzd.ru/timetable/public/?layer_id=5827&dir=0&code0=" + codeFrom + "&code1=" + codeTo + "&tfl=3&checkSeats=1&dt0=" + dateFrom + "&md=0"
            response = client.get(url, follow_redirects=True)
            rid = response.json()["RID"]
            data = {"rid": rid}
            time.sleep(4)
            data = client.post("https://pass.rzd.ru/timetable/public/ru?layer_id=5827", data=data).json()
            ans = []
            data = data["tp"][0]["list"]
            for i in data:
                if i["time0"] == timeT:
                    ans.append(i)
            if (len(ans)) == 0:
                self.answer = "Такого рейса нет"
                self.time_in_way = None
                self.train_number = None
                self.time0 = None
                self.time1 = None
                self.code0 = None
                self.code1 = None
            else:
                self.answer = "Ваш рейс найден!"
                self.time_in_way = str(ans[0]['timeInWay'])
                self.train_number = ans[0]["number"]
                self.time0 = ans[0]["time0"]
                self.time1 = ans[0]["time1"]





    def get_info(self):
        ans = {"answer": self.answer,
                "time_in_way" : self.time_in_way,
               "train_number" : self.train_number,
               "time0" : self.time0,
               "time1" : self.time1,
               "code0" : self.code0,
               "code1": self.code1
        }
        return ans
#stationTo = "Казань Пасс"
#date = "2024-12-12 00:28:00"
#dateFrom = "Москва"
#print(getInformation(stationFrom, stationTo, date))
#number = "150Х"
#print(cheker(stationFrom, stationTo, date, number))

import unittest
class Test(unittest.TestCase):

    def test_get_good_init (self):
        rightAns = {"answer": "Ваш рейс найден!",
                    "time_in_way": "13:05",
                    "train_number": "150Х",
                    "time0": "00:28",
                    "time1": "13:33",
                    "code0": "2000003",
                    "code1": "2060500"}
        ans = Train("Москва Казанская", "Казань Пасс", "2024-12-12 00:28:00").get_info()
        self.assertEqual(ans, rightAns)


    def test_get_bad_init(self):
        rightAns = {"answer": "Такого рейса нет",
                    "time_in_way": None,
                    "train_number": None,
                    "time0": None,
                    "time1": None,
                    "code0": None,
                    "code1": None}
        ans = Train("Москва Казанская", "Казань Пасс", "2024-12-12 00:27:00").get_info()
        self.assertEqual(ans, rightAns)



