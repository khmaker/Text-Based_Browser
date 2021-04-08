import os
import sys
from pathlib import Path
from argparse import ArgumentParser
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)


class Browser:
    def __init__(self):
        self.parse_directory_name()

    @staticmethod
    def parse_directory_name():
        parser = ArgumentParser()
        parser.add_argument('directory_name')
        directory_name = parser.parse_args().directory_name
        if directory_name is not None:
            Path(directory_name).mkdir(exist_ok=True)
        else:
            print('No directory name was set')
            sys.exit(0)


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
