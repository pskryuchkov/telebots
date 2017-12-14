from bs4 import BeautifulSoup
import urllib.request as ur


def load_titles(rss_link):
    rss_data = ur.urlopen(rss_link).read()
    soup = BeautifulSoup(rss_data, "xml")

    titles = []
    for x in soup.find_all('item'):
        titles.append(x.find('title').text)
        #  + " " + x.find('description').text

    return titles

sources = {"bbc": "http://feeds.bbci.co.uk/news/video_and_audio/world/rss.xml",
           "reuters": "http://feeds.reuters.com/reuters/topNews",
           "cnn": "http://rss.cnn.com/rss/edition.rss",
           "ny":  "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"}

for site in sources:

    titles = load_titles(sources[site])

    with open("../data/{}.txt".format(site), "w") as f:
        for a in titles:
            f.write(a + "\n")