import threading
from queue import Queue
from NewsSpider.spider import Spider
from NewsSpider.domain import *
from NewsSpider.general import *


class Crawler:

    def __init__(self, project_name, homepage, threads_num, parties_vocab, published_from):
        self.PROJECT_NAME = project_name
        self.HOMEPAGE = homepage
        self.DOMAIN_NAME = get_domain_name(self.HOMEPAGE)
        self.QUEUE_FILE = self.PROJECT_NAME + '/queue.txt'
        self.CRAWLED_FILE = self.PROJECT_NAME + '/crawled.txt'
        self.NUMBER_OF_THREADS = threads_num
        self.queue = Queue()
        Spider(self.PROJECT_NAME, self.HOMEPAGE, self.DOMAIN_NAME, threads_num, parties_vocab, published_from)
        self.create_workers()
        self.crawl()

    # Create worker threads (will die when main exits)
    def create_workers(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()

    # Do the next job in the queue
    def work(self):
        while True:
            url = self.queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            self.queue.task_done()

    # Each queued link is a new job
    def create_jobs(self):
        for link in file_to_set(self.QUEUE_FILE):
            self.queue.put(link)
            self.queue.join()
            self.crawl()

    # Check if there are items in the queue, if so crawl them
    def crawl(self):
        queued_links = file_to_set(self.QUEUE_FILE)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + ' links in the queue')
            self.create_jobs()
