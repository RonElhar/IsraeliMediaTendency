import sys
from datetime import date
from urllib.request import urlopen
import newspaper
from NewsSpider import crawler_main
from NewsSpider.spider import Spider
import multiprocessing
from parties_dictionary import parties_vocab



url = 'https://www.ynet.co.il/home/0,7340,L-2,00.html'
# published_from the announcement of elections
# published_until the massive rocket attack
# Elections period
# crawler_main.Crawler("ynet", url, 16, parties_vocab, published_from=date(18, 5, 1), published_until=date(30, 4, 19))
# All Time
crawler_main.Crawler("ynet", url, 16, parties_vocab, published_from=date(12, 1, 1), published_until=date(30, 5, 19))
