**AniMate**

AniMate generates anime recommendations using our recommendation algorithm  made with 
python and the _GraphQL_ api for Anilist. 
The user can input their username on Anilist and specify the number of anime recommendations that they want. 
The program will then pull 
their liked anime from their 
aniList account through the 
GraphQL api and generate anime 
recommendations through a recommendation 
algorithm. The algorithm is created by 
taking into account the user's anime's 
genre and then searching for anime on 
Anilist that fall under that particular 
genre by going through a json file that 
contains the data. The algorithm first 
generates a list of genre-based random anime, after which it sorts the list by how many of the generated anime in each category match the user's favorites in terms of studio and tags. It then produces the sorted recommendations by the recommendation algorithm
<img src="https://media.discordapp.net/attachments/1014923520649740372/1018521902412734496/unknown.png?width=606&height=532">
**Credits:** Aryan Gupta, Justin Nunag, Priyal Patel, Maya Singh