import re
from datetime import date

from bs4 import BeautifulSoup
from urllib.request import urlopen
from newspaper import Article


class NewsScraperBS(BeautifulSoup):
    def __init__(self, html_page, domain_name, base_url, **kwargs):
        super().__init__(html_page, features='html.parser')
        self.domain_name = domain_name
        self.base_url = base_url

    # <meta property="og:published_time" content="17:51 , 03.05.19">
    # <meta property="og:type" content="article">
    def is_relevant_article(self, from_date=(18, 12, 1), to_date=date(19, 5, 30)):
        return self.is_relevant_ynet(True, from_date, to_date)

    def find_links(self):
        if self.domain_name == 'ynet':
            return self.find_links_ynet()

    def is_relevant_ynet(self, filter_by_date, from_date, to_date):
        meta_type = self.find('meta', attrs={'property': re.compile("^og:type")})
        if meta_type is None or meta_type.get('content') != 'article':
            return False
        meta_published = self.find('meta', attrs={'property': re.compile("^og:published_time")})
        if meta_published is None:
            return False
        if filter_by_date and not self.is_published_after_ynet(meta_published, from_date):
            return True

    def find_links_ynet(self):
        meta_category = self.find('meta', attrs={'name': re.compile("^vr:category")})
        if meta_category is None:
            return []
        category = meta_category.get("content")
        if category != 'News' and category != 'Central':
            return []
        links = set()
        link_tags = self.findAll('a', attrs={'href': re.compile("^/articles|/home|^http://www.ynet")})
        for link_tag in link_tags:
            link = link_tag.get('href')
            if 'tags' in link:
                continue
            if link.startswith('/'):
                link = str.replace('https://ynet.co.il' + link, '\'', '')
            links.add(link)
        return links

    # <meta property="og:type" content="article">
    # <meta property="og:title" content="בהשבעת הכנסת: מאבטחי נתניהו דחפו את ריבלין ואת חיות">
    # <meta property="og:description" content="מאבטחי היחידה לאבטחת אישים, הממונים על אבטחת רה&quot;מ, דחפו שוב ושוב את נשיא המדינה ואת נשיאת העליון עד שהשניים סירבו להמשיך לצעוד עם נתניהו ואדלשטיין. ל&quot;ידיעות אחרונות&quot; נודע כי בעקבות זאת נערך בשב&quot;כ בירור. שב&quot;כ: &quot;נתחקר מול בית הנשיא&quot;. בית הנשיא: אין לנו טענות לשב&quot;כ">
    def get_article(self):
        pass

    # <meta property="og:published_time" content="07:30 , 03.05.19">
    def is_published_after_ynet(self, meta_published, from_date):
        # if not from_date is date:
        #     raise TypeError('from_date must be date object')
        date_str = str.split(str.split(meta_published.get("content"), ',')[1], '.')
        if len(date_str[2]) > 2:
            raise ValueError('year must be represented with 2 digits')
        published = date(int(date_str[2]), int(date_str[1]), int(date_str[0]))
        return from_date < published

    # def is_published_between_ynet(self, meta_published, from_date, to_date):
    #     date_str = str.split(str.split(meta_published.get("content"), ',')[1], '.')
    #     published = date(int(date_str[2]), int(date_str[1]), int(date_str[0]))
    #     return from_date < published and published < to_date

# class YnetScraper(NewsScraperBS)
# def is_published_after_ynet(from_date):
#     date_str = str.split(str.split("23.08.94", ',')[0], '.')
#     published = date(int(date_str[2]), int(date_str[1]), int(date_str[0]))
#     return from_date < published
#
#
# print(is_published_after_ynet(date(94, 8, 24)))
# print(is_published_after_ynet(date(94, 8, 22)))
