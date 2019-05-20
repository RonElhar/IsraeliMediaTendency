import threading
from urllib.request import urlopen
from newspaper import Article
from NewsSpider.domain import *
from NewsSpider.general import *
from NewsSpider.news_scraper import NewsScraperGenerator


class Spider:
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    saved_file = ''
    queue = set()
    crawled = set()
    saved = set()
    published_from = None
    published_until = None
    subjects_vocab = {}
    parties_locks = {}

    def __init__(self, project_name, base_url, domain_name, lines_count, parties_vocab, published_from,
                 published_until):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.saved_file = Spider.project_name + '/saved.txt'
        Spider.site_file_lines_count = lines_count
        Spider.subjects_vocab = parties_vocab
        Spider.published_from = published_from
        Spider.published_until = published_until
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
        Spider.saved = file_to_set(Spider.saved_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)) + ' | Saved ' + str(
                len(Spider.saved)))
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
            scraper = NewsScraperGenerator(html_string, Spider.domain_name, Spider.base_url).generate()
            # finder = NewsScraperBS(html_string, Spider.domain_name, Spider.base_url)
            if 'articles' in page_url and scraper.is_relevant_article(Spider.published_from,
                                                                      Spider.published_until):
                Spider.save_article(page_url)
        except Exception as e:
            print(str(e))
            return set()
        links = scraper.find_links()
        return links

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
        set_to_file(Spider.saved, Spider.saved_file)
    # save article - saves the article to the appropriate file if it's relevant to the party
    @staticmethod
    def save_article(url):
        article = Article(url)
        article.download()
        article.parse()
        summary = article.title + " " + article.meta_description
        for subject in Spider.subjects_vocab:
            for word in Spider.subjects_vocab[subject]:
                if word in summary:
                    Spider.parties_locks[subject].acquire()
                    Spider.save_article_to_subject_file(article, subject)
                    Spider.parties_locks[subject].release()
                    Spider.saved.add(url)
                    break
    # writes the article to a file
    @staticmethod
    def save_article_to_subject_file(article, subject):

        file_lines = [article.title]
        article_txt = str.split(article.text, '\n')
        for line in article_txt:
            line.replace('\n', '')
            if not line == "":
                file_lines.append(line + '\n')
        # file_lines.append('</article>\n')
        with open(Spider.project_name + '\\' + subject + '.txt', 'a+', encoding='utf-8') as f:
            for line in file_lines:
                f.write(line)
