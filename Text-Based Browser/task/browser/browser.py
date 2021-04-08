import os
import argparse
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)


def make_directory():
    global dir_name
    parser = argparse.ArgumentParser()
    parser.add_argument('dir')
    args = vars(parser.parse_args())
    dir_name = args['dir']
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def write_file(n):
    global current
    name = '.'.join(n.split('.')[:-1])
    resp = requests.get(f'https://{n}')
    soup = BeautifulSoup(resp.text, 'html.parser')
    with open(f'{dir_name}/{name}.txt', 'w', encoding='utf-8') as file:
        for string in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']):
            file.write(string.get_text())
            if string.name == 'a':
                print(Fore.BLUE + string.get_text())
            else:
                print(string.get_text())
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
    pass


make_directory()
files = set()
history = []
current = ''

if __name__ == '__main__':
    call_url()
