from urllib.request import urlopen

import newspaper

from NewsSpider import crawler_main
from NewsSpider.spider import Spider

# page_url = "https://www.ynet.co.il/articles/0,7340,L-5500186,00.html#autoplay"
# Spider.save_article(page_url)

parties_vocab = {'ליכוד': ['ליכוד', 'רגב', 'ישראל כץ', 'ארדן', 'אדלשטיין', 'נתניהו', 'ביבי'],
                 'איחוד הימין': ['איחוד מפלגות הימין', 'איחוד הימין', 'סמוטריץ', 'איתמר בן גביר', 'פרץ'],
                 'כחול לבן': ['לפיד', 'גבי אשכנזי', 'בוגי יעלון', 'גנץ'],
                 'עבודה': ['שמולי', 'אבי גבאי'],
                 'ש"ס': ["דרעי"]}
url = 'https://www.ynet.co.il/home/0,7340,L-317,00.html'
crawler_main.Crawler("ynet", url, 8, parties_vocab)
#
# cnn_paper = newspaper.build('http://walla.co.il')
#
# for category in cnn_paper.category_urls():
#      print(category)
#