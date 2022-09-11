import json
import random
import streamlit as st
from itertools import cycle
import login
import animeInfo

# given the user's anime list, choose a random anime to pull the recommendations from
def randomChooseAnime(animeList):
    animeArray = []
    for x in animeList.keys():
        animeArray.append(x)
    chosenAnime = random.choice(animeArray)
    return chosenAnime


# with the chosen anime, go to that genre and pull the number of anime the user wants recommended
def getAnimeFromGenre(animeList, chosenAnime, numberOfAnime):
    genres = animeList[chosenAnime][1]
    chosenGenre = random.choice(genres)

    animeByGenre = open("get_anime_query.json")
    data = json.load(animeByGenre)

    listOfAnime = data[chosenGenre.lower()]
    listOfAnime = random.sample(listOfAnime, numberOfAnime)

    return listOfAnime


# the algorithm that determines what anime to recommend based on a points system
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

    # algorithm: animeScore = studioMatching + tagMatching
    # tagMatching = tagNum / 2

    # initalizing the dicionary
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
                importance = usersTags[x]
                currentRanking = animeRanking[key] + importance
                animeRanking[key] = currentRanking

    file = open("anime_by_id.json")
    animeName = json.load(file)

    animeRanking = sorted(animeRanking.items(), key=lambda x: x[1], reverse=True)

    # loads the images with the anime name
    animeImagewWithName = dict()
    for anime in animeRanking:
        image = animeName[anime[0]]["cover_image"]
        if animeName[anime[0]]["name_english"] is None:
            animeImagewWithName[animeName[anime[0]]["name_romaji"]] = image
        else:
            animeImagewWithName[animeName[anime[0]]["name_english"]] = image

    # loads the image in streamlit front end
    filteredImages = list(animeImagewWithName.values())
    caption = list(animeImagewWithName.keys())
    cols = cycle(st.columns(4))
    for idx, filteredImage in enumerate(filteredImages):
        next(cols).image(filteredImage, width=150, caption=caption[idx])


def algo(username, numOfRecs):
    animeList = animeInfo.getUserAnime(login.getUserAnimeList(login.getUserID(username)))
    recommendationAlgorithm(getAnimeFromGenre(animeList, randomChooseAnime(animeList), int(numOfRecs)), username)
