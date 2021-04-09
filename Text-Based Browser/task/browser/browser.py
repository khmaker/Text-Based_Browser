# coding=utf-8
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from shutil import rmtree

import requests
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init

init(autoreset=True)


class Browser:
    tags = ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li')

    def __init__(self):
        self.directory_name = None
        self.__parse_directory_name()
        self.history = []
        self.cache = set()
        self.url = None
        self.current_page = None
        self.dispatcher()

    def dispatcher(self):
        user_input = input()
        if user_input in ('back', 'exit'):
            {'back': self.__back, 'exit': self.__exit}.get(user_input)()

    def __parse_directory_name(self):
        parser = ArgumentParser()
        parser.add_argument('directory_name')
        directory_name = parser.parse_args().directory_name
        if directory_name is not None:
            Path(directory_name).mkdir(exist_ok=True)
            self.directory_name = directory_name
        else:
            self.__exit('No directory name was set')

    def __exit(self, message=None):
        print(message if message is not None else '')
        rmtree(Path(self.directory_name))
        sys.exit(0)

    def make_soup(self):
        pass

    def __back(self):
        if not self.history:
            print('History is empty')
        else:
            last_history_item = self.history.pop()
            with open(f'{self.directory_name}/{last_history_item}.txt',
                      'r',
                      encoding='utf-8') as file:
                print(file.read())
        return self.dispatcher()

    def __write_file(self, soup=None):
        # TODO: split file handling and print
        if soup is not None:
            with open(f'{self.directory_name}/{self.url}.txt',
                      'w',
                      encoding='utf-8') as file:
                for string in soup.find_all(self.tags):
                    text = string.get_text()
                    file.write(text)
                    print(Fore.BLUE + text if string.name == 'a' else text)


def make_directory():
    global dir_name
    parser = ArgumentParser()
    parser.add_argument('dir')
    dir_name = parser.parse_args().dir
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def write_file(n):
    global current
    name = '.'.join(n.split('.')[:-1])
    resp = requests.get(f'https://{n}')
    soup = BeautifulSoup(resp.text, 'html.parser')
    with open(f'{dir_name}/{name}.txt', 'w', encoding='utf-8') as file:
        tags = ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li')
        for string in soup.find_all(tags):
            text = string.get_text()
            file.write(text)
            print(Fore.BLUE + text if string.name == 'a' else text)

    files.add(name)
    if current:
        history.append(current)
    current = name
    return call_url()


def call_url():
    n = input()
    if '.' in n:
        write_file(n)
    elif n == 'exit':
        return
    elif n in files:
        return call_file(n)
    elif n == 'back':
        return call_back()
    else:
        print('Error: Incorrect URL')
        return call_url()


def call_file(name):
    global current
    with open(f'{dir_name}/{name}.txt', 'r', encoding='utf-8') as file:
        print(file.read())
    history.append(current)
    current = name
    return call_url()


def call_back():
    if history:
        with open(f'{dir_name}/{history.pop()}.txt', 'r', encoding='utf-8') as file:
            print(file.read())
        return call_url()


make_directory()
files = set()
history = []
current = ''

if __name__ == '__main__':
    call_url()
