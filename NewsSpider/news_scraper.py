import re
from datetime import date

from bs4 import BeautifulSoup
from abc import abstractmethod

class NewsScraperBS(BeautifulSoup):
    def __init__(self, html_page, domain_name, base_url, **kwargs):
        super().__init__(html_page, features='html.parser')
        self.domain_name = domain_name
        self.base_url = base_url

    @abstractmethod
    def find_links(self):
        if self.domain_name == 'ynet':
            return self.find_links_ynet()

    @abstractmethod
    def is_relevant_article(self, from_date, until_date):
        return self.is_relevant_ynet(from_date, until_date)

    @abstractmethod
    def is_published_between(self, meta_published, from_date, until_date):
        pass


class YnetScraper(NewsScraperBS):

    def __init__(self, html_page, base_url, **kwargs):
        super(YnetScraper, self).__init__(html_page, "ynet", base_url, **kwargs)

    def find_links(self):
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

    def is_relevant_article(self, from_date, until_date):
        meta_type = self.find('meta', attrs={'property': re.compile("^og:type")})
        if meta_type is None or meta_type.get('content') != 'article':
            return False
        meta_published = self.find('meta', attrs={'property': re.compile("^og:published_time")})
        if meta_published is None:
            return False
        if not self.is_published_between(meta_published, from_date, until_date):
            return False
        return True

    def is_published_between(self, meta_published, from_date, until_date):
        date_str = str.split(str.split(meta_published.get("content"), ',')[1], '.')
        published = date(int(date_str[2]), int(date_str[1]), int(date_str[0]))
        return from_date <= published <= until_date

    def insert_before(self, successor):
        pass

    def insert_after(self, successor):
        pass


class NewsScraperGenerator:
    def __init__(self, html_page, domain_name, base_url, **kwargs):
        self.html_page = html_page
        self.domain_name = domain_name
        self.base_url = base_url
        self.kwargs = kwargs

    def generate(self):
        if self.domain_name == 'ynet':
            return YnetScraper(self.html_page, self.base_url, **self.kwargs)

# print(is_published_after_ynet(date(94, 8, 24)))
# print(is_published_after_ynet(date(94, 8, 22)))
# <meta property="og:type" content="article">
# <meta property="og:title" content="בהשבעת הכנסת: מאבטחי נתניהו דחפו את ריבלין ואת חיות">
# <meta property="og:description" content="מאבטחי היחידה לאבטחת אישים, הממונים על אבטחת רה&quot;מ, דחפו שוב ושוב את נשיא המדינה ואת נשיאת העליון עד שהשניים סירבו להמשיך לצעוד עם נתניהו ואדלשטיין. ל&quot;ידיעות אחרונות&quot; נודע כי בעקבות זאת נערך בשב&quot;כ בירור. שב&quot;כ: &quot;נתחקר מול בית הנשיא&quot;. בית הנשיא: אין לנו טענות לשב&quot;כ">
# <meta property="og:published_time" content="07:30 , 03.05.19">
