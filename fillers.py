from bs4 import BeautifulSoup
import requests

def getLinks():
    links = []

    anime = requests.get("http://www.animefillerlist.com/shows").content
    soup = BeautifulSoup(anime, 'html.parser')
    root = soup.findAll('div', attrs = { "id": "ShowList" })

    for link in root[0].find_all('a'):
        links.append(f"http://www.animefillerlist.com{link.get('href')}")
    
    return links

def getFillers():
    fillers = {}
    links = getLinks()

    for link in links:
        anime = requests.get(link).content
        soup = BeautifulSoup(anime, 'html.parser')
        name = soup.find('h1').string.split(" Filler List")[0]

        fillers[name] = { "name": name, "fillers": [], "mixed": [] }

        episodes = soup.find('table', { "class": "EpisodeList" })

        if episodes:
            fillers_even = episodes.findAll('tr', { "class": "filler even" })
            fillers_odd = episodes.findAll('tr', { "class": "filler odd" })

            mixed_even = episodes.findAll('tr', { "class": "mixed_canon/filler even" })
            mixed_odd = episodes.findAll('tr', { "class": "mixed_canon/filler odd" })

            for episode in fillers_even:
                episode = episode.find('td', { "class": "Number" })

                fillers[name]["fillers"].append(episode.string)

            for episode in fillers_odd:
                episode = episode.find('td', { "class": "Number" })

                fillers[name]["fillers"].append(episode.string)


            for episode in mixed_even:
                episode = episode.find('td', { "class": "Number" })

                fillers[name]["mixed"].append(episode.string)

            for episode in mixed_odd:
                episode = episode.find('td', { "class": "Number" })

                fillers[name]["mixed"].append(episode.string)
        
    return fillers