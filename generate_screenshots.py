import os
import logging
import requests
import yaml
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

    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.repo_data = self.retrieve_repo_data(repo_url)
        self.screenshot = None

    @staticmethod
    def retrieve_repo_data(repo_url):
        api_path = '{0}{1}'.format(Repository.REPO_API_PATH, urlparse(repo_url).path)
        return requests.get(api_path).json()

class Screenshotter(object):
    def __init__(self,
                 repository_urls,
                 width=1280,
                 height=800,
                 screenshot_directory='screenshots',
                 screenshot_format='png',
                 data_dump_directory='_data',
                 logger=default_logger):
        self.repositories = [Repository(url) for url in repository_urls]
        self.width = width
        self.height = height
        self.screenshot_directory = screenshot_directory
        self.screenshot_format = screenshot_format
        self.driver = None
        self.data_dump_directory = data_dump_directory
        self.logger = logger
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(get_log_handler())

    def __enter__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(self.width, self.height)
        return self

    def __exit__(self, *args):
        self.driver.quit()

    def capture_screenshot(self, repository):
        self.driver.get(repository.repo_data['homepage'])
        self.logger.info('finished: {}'.format(repository.repo_data['name']))
        return self.driver.save_screenshot(self.screenshot_path(repository))

    def screenshot_path(self, repository):
        file_name = '{0}.{1}'.format(repository.repo_data['name'], self.screenshot_format)
        return os.path.join(self.screenshot_directory, file_name)

    def run(self):
        for repo in self.repositories:
            repo.screenshot = self.capture_screenshot(repo)
        self.logger.info('All finished!')

    def dump_repo_data(self):
        formatted_data = {repo.repo_data['name']: repo.repo_data for repo in self.repositories}
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
