# coding=utf-8
import sys
from argparse import ArgumentParser
from pathlib import Path

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
        self.current_page = None
        self.dispatcher()

    def __parse_directory_name(self):
        parser = ArgumentParser()
        parser.add_argument('directory_name')
        directory_name = parser.parse_args().directory_name
        if directory_name is not None:
            Path(directory_name).mkdir(exist_ok=True)
            self.directory_name = directory_name
        else:
            self.__exit('No directory name was set')

    def dispatcher(self):
        user_input = input()
        if user_input in ('back', 'exit'):
            {'back': self.__back, 'exit': self.__exit}.get(user_input)()
        if user_input in self.cache:
            self.__open_file(user_input)
            return self.dispatcher()
        self.process_user_input(user_input)

    def process_user_input(self, user_input):
        if '.' not in user_input:
            print('Error: Incorrect URL')
            return self.dispatcher()
        self.__get_page(user_input)
        self.__print_file()
        filename, _, _ = user_input.rpartition('.')
        self.__write_file(filename)
        self.cache.add(filename)
        return self.dispatcher()

    def __get_page(self, user_input):
        try:
            self.current_page = requests.get(f'https://' + user_input).text
        except requests.exceptions.RequestException as e:
            print(e)
            return self.dispatcher()

    @staticmethod
    def __exit(message=None):
        print(message if message is not None else '')
        sys.exit(0)

    def make_soup(self):
        return BeautifulSoup(self.current_page, 'html.parser')

    def __back(self):
        if not self.history:
            print('History is empty')
        else:
            self.current_page = self.__open_file(self.history.pop())
        return self.dispatcher()

    def __write_file(self, filename):
        with open(f'{self.directory_name}/{filename}.txt',
                  'w',
                  encoding='utf-8') as file:
            file.write(self.current_page)

    def __open_file(self, filename):
        with open(f'{self.directory_name}/{filename}.txt',
                  'r',
                  encoding='utf-8') as file:
            return file.read()

    def __print_file(self):
        soup = self.make_soup()
        for string in soup.find_all(self.tags):
            text = string.get_text()
            print(Fore.BLUE + text if string.name == 'a' else text)


if __name__ == '__main__':
    # call_url()
    Browser()
