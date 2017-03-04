import os
import logging
import requests
import shutil
import yaml
from datetime import datetime
from selenium import webdriver
from urllib.parse import urlparse
import __main__

default_logger = logging.getLogger(__main__.__file__)

def get_log_handler():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    return handler

class Repository(object):
    REPO_API_PATH = 'https://api.github.com/repos'

    def __init__(self, repo_data):
        self.screenshot = None
        for k, v in repo_data.items():
            setattr(self, k, v)

    @classmethod
    def from_url(cls, repo_url):
        api_path = '{0}{1}'.format(Repository.REPO_API_PATH, urlparse(repo_url).path)
        return cls(requests.get(api_path).json())

class Screenshotter(object):
    def __init__(self,
                 repository_urls,
                 width=1280,
                 height=800,
                 screenshot_directory='screenshots',
                 screenshot_format='png',
                 data_dump_directory='_data',
                 logger=default_logger):
        self.repositories = [Repository.from_url(url) for url in repository_urls]
        self.width = width
        self.height = height
        self.screenshot_directory = screenshot_directory
        self.screenshot_format = screenshot_format
        self.driver = None
        self.data_dump_directory = data_dump_directory
        self.logger = logger
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(get_log_handler())
        self.init_time = datetime.utcnow().replace(microsecond=0).isoformat()

    def __enter__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(self.width, self.height)
        return self

    def __exit__(self, *args):
        self.driver.quit()

    def clear_screenshot_directory(self):
        for f in os.listdir(self.screenshot_directory):
            if not f.endswith('.keep'):
                os.remove(os.path.join(self.screenshot_directory, f))

    def capture_screenshot(self, repository):
        self.driver.get(repository.homepage)
        self.logger.info('finished: {}'.format(repository.name))
        return self.driver.save_screenshot(self.screenshot_path(repository))

    def screenshot_path(self, repository):
        file_name = '{}_{}.{}'.format(
            repository.name,
            self.init_time,
            self.screenshot_format,
        )
        return os.path.join(self.screenshot_directory, file_name)

    def run(self):
        self.clear_screenshot_directory()
        for repo in self.repositories:
            repo.screenshot = self.capture_screenshot(repo)
        self.logger.info('All finished!')

    def dump_repo_data(self):
        formatted_data = {repo.name: repo.__dict__ for repo in self.repositories}
        export_path = os.path.join(self.data_dump_directory, 'repo_data.yml')
        with open(export_path, 'w') as ef:
            yaml.dump(formatted_data, ef, default_flow_style=False)
        self.logger.info('Finsihed Dumping')

if __name__ == '__main__':
    repository_urls = [
        'https://github.com/cscanlin/munger-builder',
        'https://github.com/cscanlin/choice-optimizer',
        'https://github.com/cscanlin/minesweeper',
        'https://github.com/cscanlin/periodic-table-timeline',
    ]
    with Screenshotter(repository_urls) as ss:
        ss.run()
        ss.dump_repo_data()
