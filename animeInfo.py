import json
import login
import requests


def getStudio(animeList):
    studios = set()
    for s in animeList["data"]["anime"]["mediaList"]:
        studioName = s["media"]["studios"]["nodes"]
        for x in studioName:
            studios.add(x["name"])
    return studios


def getTags(userStats):
    tags = dict()
    info = userStats["data"]["User"]["statistics"]["anime"]["tags"]
    for x in info:
        tagName = x["tag"]["name"]
        tagCount = x["count"]
        tags[tagName] = tagCount
    # print(info)
    # print(tags)

    return tags


def getGenre(animeList):
    genre_list = []
    genre_dict = {}

    subfile = animeList["data"]["anime"]["mediaList"]
    for anime in subfile:
        genres = anime["media"]["genres"]
        for x in genres:
            genre_list.append(x)
    for i in genre_list:
        if i not in genre_dict:
            genre_dict[i] = 1
        else:
            genre_dict[i] += 1
    return genre_dict


def getUserAnime(animeList):
    userAnimeList = dict()
    for anime in animeList["data"]["anime"]["mediaList"]:
        animeName = anime["media"]["title"]["english"]
        animeID = anime["media"]["id"]
        animeGenre = anime["media"]["genres"]
        userAnimeList[animeName] = [animeID, animeGenre]
    return userAnimeList


def getAnimeStudio(animeID):
    query = """\
            query ($id: Int) {
                Media(id: $id, type: ANIME) {
                    studios 
                    {
                        nodes 
                        {
                            name
                        }
                    }
                }
            }
        """

    url = 'https://graphql.anilist.co'

    variables = {
        'id': animeID
    }
    response = requests.post(
        url,
        json={'query': query, 'variables': variables}
    )

    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    studioList = json.loads(response.text)
    studios = set()

    # prints studios of each 10 anime with tag as its key and studios as values
    studio = studioList["data"]["Media"]["studios"]["nodes"]
    for x in studio:
        studios.add(x["name"])

    return studios


def getAnimeTag(id):
    query = """\
    query ($id: Int) {
        Media(id: $id, type: ANIME) {
            tags {
            name
            }
        }
    }
    """
    # Define our query variables and values that will be used in the query request
    variables = {
        'id': id
    }
    url = 'https://graphql.anilist.co'
    # Make the HTTP Api request
    response = requests.post(
        url,
        json={'query': query, 'variables': variables}
    )
    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    file = json.loads(response.text)

    return file['data']['Media']['tags']

