
import requests

URL = "https://kitsu.io/api/edge/anime?page[limit]=3&page[offset]=0&{}"

class AnimeInfo:
    def __init__(self,title, synopsis, description, episodeCount, startDate, endDate, ageRating, status, showType):
        self.title = title
        self.synopsis = synopsis
        self.description = description
        self.episodeCount = episodeCount
        self.startDate = startDate
        self.endDate = endDate
        self.ageRating = ageRating
        self.status = status
        self.showType = showType


def filter_categories(queries):
    query = "filter[categories]={}".format(queries)
    res = requests.get(URL.format(query))
    data = res.json()["data"]
    return data

def filter_text(queries):
    query = "filter[text]={}".format(queries)
    res = requests.get(URL.format(query))
    data = res.json()
    return data

def get_anime_list(data):
    animeList = []

    for anime in data['data']:
        attrib = anime['attributes']
        animeInfo = AnimeInfo(attrib['titles']['en_jp'],attrib['synopsis'],attrib['description'],attrib['episodeCount'],attrib['startDate'],attrib['endDate'],attrib['ageRating'],attrib['status'],attrib['showType'])
        prntFormat = """
```Title:{0.title}\n
start date:{1.startDate}\tend date:{2.endDate}\n
episodes:{3.episodeCount}\tstatus:{4.status}\tshow type:{5.showType}\n
Synopsis:
\t{6.synopsis}```""".format(animeInfo,animeInfo,animeInfo,animeInfo,animeInfo,animeInfo,animeInfo)

        animeList.append(prntFormat)

    return animeList

def get_total_result(data):
  return data['meta']['count']

def next_page(pagination):
    res = requests.get(pagination['next'])
    data = res.json()
    return data

def prev_page(pagination):
    res = requests.get(pagination['prev'])
    data = res.json()
    return data

def first_page(pagination):
    res = requests.get(pagination['first'])
    data = res.json()
    return data

def last_page(pagination):
    res = requests.get(pagination['last'])
    data = res.json()
    return data

def suggest_anime():
    pass
