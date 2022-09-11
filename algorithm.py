import json
import random
import requests

import login
import animeInfo

# randomly select one anime from the user list
# take the genre from the anime and extract 10 anime from the list
# go through each anime -> if they have the same tags add 1 point if they have the same studio add 1 point
# the top2 anime with the most points gets chosen to show as a rec
# the next top anime would be shown


def randomChooseAnime(animeList):
    animeArray = []
    for x in animeList.keys():
        animeArray.append(x)
    chosenAnime = random.choice(animeArray)
    return chosenAnime


def getAnimeFromGenre(animeList, chosenAnime, numberOfAnime):
    genres = animeList[chosenAnime][1]
    chosenGenre = random.choice(genres)

    animeByGenre = open("get_anime_query")
    data = json.load(animeByGenre)

    listOfAnime = data[chosenGenre.lower()]
    listOfAnime = random.sample(listOfAnime, numberOfAnime)

    return listOfAnime


def recommendationAlgorithm(listOfAnime, username):
    top10Anime = listOfAnime
    animeStudio = dict()

    # getting the studios from each anime and putting into a dictionary
    # dict() for animeID -> num of Studios overlap
    studiosOverlap = dict()

    for studio in top10Anime:
        try:
            entry = animeInfo.getAnimeTag(studio)
        except TypeError:
            return
        animeStudio[studio] = entry
        # initialize overlaps to 0
        studiosOverlap[studio] = 0

    # collecting the tags of each anime
    tags = dict()

    for x in top10Anime:
        try:
            animeTags = animeInfo.getAnimeTag(x)
        except TypeError:
            return
        tagArray = []
        for tag in animeTags:
            tagArray.append(tag["name"])
        tags[x] = tagArray

    # gets all the studios and tags from the animeList of the user
    userStudios = animeInfo.getStudio(login.getUserAnimeList(login.getUserID(username)))
    usersTags = animeInfo.getTags(login.getUserStats(username))

    #print(animeStudio)
    #print(tags)
    #print(userStudios)
    #print(usersTags)

    # algorithm: animeScore = studioMatching + tagMatching
    # tagMatching = tagNum / 2

    animeRanking = dict()
    for x in animeStudio.keys():
        animeRanking[x] = 0

    # get the number of same studios
    for studio in userStudios:
        for key, value in animeStudio.items():
            if studio in value:
                animeRanking[key] = animeRanking[key] + 1

    # get the number of same tags
    for x in usersTags.keys():
        for key, value in tags.items():
            if x in value:
                importance = usersTags[x] / 2
                currentRanking = animeRanking[key] + importance
                animeRanking[key] = currentRanking

    file = open("anime_by_id.json")
    animeName = json.load(file)

    idToNameDict = dict()
    for x in animeRanking.keys():
        if animeName[x]["name_english"] is None:
            idToNameDict[animeName[x]["name_romaji"]] = animeRanking[x]
        else:
            idToNameDict[animeName[x]["name_english"]] = animeRanking[x]

    print(idToNameDict)


def algo(username):
    animeList = animeInfo.getUserAnime(login.getUserAnimeList(login.getUserID(username)))
    numberOfAnime = input("How many shows do you want recommended? ")
    recommendationAlgorithm(getAnimeFromGenre(animeList, randomChooseAnime(animeList), int(numberOfAnime)), username)
