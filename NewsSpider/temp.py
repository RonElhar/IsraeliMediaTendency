# exec(open("C:\\Users\\USER\\Desktop\\IsraeliMediaTendency\\main.py",encoding="utf8").read())
import os

# ROOT_DIR = os.path.dirname(os.path.dirname())  # This is your Project Root
# print(ROOT_DIR)

ROOT_DIR = os.path.realpath(__file__)

print(ROOT_DIR)

# url = "https://www.ynet.co.il/home/0,7340,L-185,00.html"
# page = urlopen("https://www.ynet.co.il/articles/0,7340,L-5503107,00.html")
# link_finder = newsScrapperBS(page, 'ynet', base_url="https://www.ynet.co.il")
# print(link_finder.is_relevant_article())
# links = link_finder.find_links()
# for link in links:
#     print(link)
# article = Article('https://www.ynet.co.il/articles/0,7340,L-5500977,00.html')
# article.download()
# article.parse()
# print(article.text)
# soup = BeautifulSoup(html_page, 'html.parser')
# meta_category = soup.find('meta', attrs={'name': re.compile("^vr:category")})
# category = meta_category.get("content")
# print(category)
# article_links = soup.findAll('a', attrs={'href': re.compile("^/articles")})
# for link in article_links:
#     print(link.get('href'))
# other_links = soup.findAll('a', attrs={'href': re.compile("^/home")})
# for link in other_links:
#     print(link.get('href'))
# more_links = soup.findAll('a', attrs={'href': re.compile("^http://www.ynet")})
# for link in more_links:
#     print(link.get('href'))

# article_links.extend(other_links)
# print(article_links)
# links = []
# links.extend(article_links.extend(other_links)).extend(more_links)

# print(links)