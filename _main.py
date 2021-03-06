"""
##### TXT Miner #####
"""
# Requests is needed to request page from websites
# Retrieving news articles w/ beautifulsoup and requests
# Pandas to create a df
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime

# Function that returns number of words in a string
def word_count(input):
    conversion = ""
    for i in input:
        if i in " '-’":
            conversion = conversion + i + "\n"
        else:
            conversion = conversion + i
    return len(conversion.splitlines())

# Current date and time
now = datetime.now()
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

# Where to return results on PC & output files title info
path = r"C:\Users\jbmor\Desktop\TRA3601_corpus\games_FR\\"
prefix = "NINTENDO_games_"
language = "_FR"

# Variables needed to create df
file_name_list = []
title_list = []
content_list = []
nb_words_list = []
url_list = []

# Gets article links from NINTENDO and creates a list
page_total = 50
page_first = 1
x = True
article_url_list = []
article_title_list = []
article_list = {
        "title": [],
        "url": [],
    }

while x:
    news = rf"https://www.nintendo.com/fr-ca/store/games/?p={page_first}&sort=rd"
    data_news = requests.get(news)
    print(data_news)
    soup_news = bs(data_news.text, "html.parser")
    article_list_parent = soup_news.find_all("a", class_="BasicTilestyles__LinkWrapper-sc-sh8sf3-12 bQmYHg")
    try:
        if page_first <= page_total:
            for i in article_list_parent:
                url_html = i["href"]
                title_html = url_html.replace("/en-ca/store/products/", "")
                article_list["url"].append(url_html)
                article_list["title"].append(title_html)
                print(title_html)
            page_first = page_first + 1

        else:
             x = False

    except KeyError as err1:
        print(err1)
        x = False
        page_first = page_first + 1

article_url_list = article_list["url"]
article_title_list = article_list["title"]
print(article_url_list)
print(article_title_list)

# Retrieves articles with web scraping script and writes new files in specified directory (path)
index = 0
for article_url in article_url_list:
    url = "https://www.nintendo.com/" + article_url
    file_name = prefix + article_title_list[index] + language
    file_name = file_name.replace(r"/", "")
    file_name = file_name.replace(r"!", "")
    file_name = file_name.replace(r"?", "")
    file_name = file_name.replace(r".", "")
    file_name = file_name.replace(r":", "")
    file_name = file_name.replace("\"", "")
    index = index + 1
    with open(path + file_name + ".txt", "w", encoding="UTF-8") as output:
            try:
                # HTML parser : retrieves title, description, article, etc. from specified URL
                # Setting up BeautifulSoup - Requests from url w/ .get() method & parsing
                data = requests.get(url)
                soup = bs(data.text, "html.parser")

                # Retrieves interesting info from soup (each article HTML page)
                title = soup.find("h1", class_="Headingstyles__StyledH-sc-qpned7-0 HUGKw")
                paragraphs = soup.find("div", class_="RichTextstyles__Html-sc-1ensjc6-0 iRSUJV")

                # Retrieves text from retrieved info
                title_text = title.get_text()
                content_text = paragraphs.text

                # Adds title and paragraphs to the content variable
                # Writes it in new file (output)
                article = title_text + "\n" + content_text
                output.write(article)

                # Appends all interesting info to corresponding list (needed for df)
                file_name_list.append(file_name)
                title_list.append(title_text)
                content_list.append(content_text)
                nb_words_list.append(word_count(article))
                url_list.append(url)

            except UnicodeEncodeError as err2:
                print(err2)
                pass
            except AttributeError as err3:
                print(err3)
                pass
            except OSError as err4:
                print(err4)
                pass

# Creates pandas df from interesting data lists and specified columns
df = pd.DataFrame({
    "file name": file_name_list,
    "title": title_list,
    "content": content_list,
    "Nb. words": nb_words_list,
    "URL": url_list,
})

df.to_csv(path + "_corpus_" + str(date_time) + ".csv", index=False, sep="\t")
