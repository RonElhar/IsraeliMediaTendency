from urllib.request import urlopen

from NewsSpider.spider import Spider

page_url = "https://www.ynet.co.il/articles/0,7340,L-5500186,00.html#autoplay"
# response = urlopen(page_url)
# if 'text/html' in response.getheader('Content-Type'):
#     html_bytes = response.read()
#     html_string = html_bytes.decode("utf-8")
Spider.save_article(page_url)
