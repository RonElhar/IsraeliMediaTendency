import threading
from urllib.request import urlopen
from bs4 import BeautifulSoup
from idna import unicode
from newspaper import Article

from NewsSpider.link_finder import LinkFinder
from NewsSpider.domain import *
from NewsSpider.general import *


class Spider:
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    site_file_lines_count = 1
    parties_vocab = {}
    parties_locks = {}

    def __init__(self, project_name, base_url, domain_name, lines_count, parties_vocab):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.site_file_lines_count = lines_count
        Spider.parties_vocab = parties_vocab
        self.boot()
        self.crawl_page('First spider', Spider.base_url)
        for party in parties_vocab:
            Spider.parties_locks[party] = threading.Lock()

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                # only for ynet:
                if 'articles' in page_url:
                    Spider.save_article(page_url)
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            # print(get_domain_name(url))
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    @staticmethod
    def save_article(url):
        article = Article(url)
        article.download()
        article.parse()
        summary = article.title + " " + article.meta_description
        # TODO: decide on which period of time wer'e working
        # if article.text == "" or (article.publish_date.year < 2019 and article.publish_date.month < 10) or (
        #         article.publish_date.year == 2019 and article.publish_date.day > 9):
        #     return
        for party in Spider.parties_vocab:
            for word in Spider.parties_vocab[party]:
                if word in summary:
                    Spider.parties_locks[party].acquire()
                    Spider.save_article_to_party_file(article.text, article.title, party)
                    Spider.parties_locks[party].release()
                    break

    @staticmethod
    def save_article_to_site_file(line_number, article_text, article_title):
        text = []
        temp_text = ['<article>', article_title]
        temp_text.extend(str.split(article_text, '\n'))
        for line in temp_text:
            line.replace('\n', '')
            if not line == "":
                text.append(line)
        text.append('</article>')
        with open(Spider.project_name + '\\articles.txt', 'a+', encoding='utf-8') as f:
            f.seek(line_number)
            for line in text:
                f.write(line + '\n')
        Spider.site_file_lines_count += len(text)
        return len(text)

    @staticmethod
    def save_article_to_party_file(article_text, article_title, party):
        text = []
        temp_text = [article_title]
        temp_text.extend(str.split(article_text, '\n'))
        for line in temp_text:
            line.replace('\n', '')
            if not line == "":
                text.append(line)
        # text.append('</article>')
        with open(Spider.project_name + '\\' + party + '.txt', 'a+', encoding='utf-8') as f:
            for line in text:
                f.write(line + '\n')
