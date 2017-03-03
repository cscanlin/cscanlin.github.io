import os
import requests
from selenium import webdriver
from urlparse import urlparse

WIDTH, HEIGHT = 1024, 768
REPOSITORY_URLS = [
    'https://github.com/cscanlin/munger-builder',
    'https://github.com/cscanlin/choice-optimizer',
    'https://github.com/cscanlin/minesweeper',
    'https://github.com/cscanlin/periodic-table-timeline',
]

def retrieve_repo_data(repo_url):
    api_path = 'https://api.github.com/repos{}'.format(urlparse(repo_url)['path'])
    return requests.get(api_path).json()

def capture_screenshot(repo_data, output_directory='images'):
    driver.get(repo_data['homepage'])
    screenshot_path = os.path.join(output_directory, '{}.png'.format(repo_data['name']))
    driver.save_screenshot(screenshot_path)
    print('finished: {}'.format(repo_data['name']))

if __name__ == '__main__':
    driver = webdriver.PhantomJS()
    driver.set_window_size(WIDTH, HEIGHT)
    for url in REPOSITORY_URLS:
        print(url)
        repo_data = retrieve_repo_data(url)
        print(repo_data)
        capture_screenshot(repo_data)
    driver.quit()
