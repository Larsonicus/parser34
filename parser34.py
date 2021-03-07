import requests
from bs4 import BeautifulSoup
from random import choice

url = f'https://rule34.xxx/index.php?page=post&s=list&tags={input("Введите тэг: ")}+-gay'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4414.0 '
                         'Safari/537.36 Edg/90.0.803.0', 'accept': '*/*'}
HOST = 'https://rule34.xxx/'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_='pagination')
    try:
        p = pagination.find_all('a')
        pages = [url]
        for page in p:
            pages.append(HOST + (page.get('href')))
    except AttributeError:
        pages = None
    return pages


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('span', class_='thumb')
    links = []
    for i in items:
        links.append(HOST + i.find('a').get('href'))
    return links


def get_image(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='flexi')
    image = []
    for i in items:
        try:
            image.append(i.find('img', alt_='').get('src'))
        except AttributeError:
            print('None')
    return image


def parse():
    html = get_html(url)
    pages_links = get_pages_count(html.text)
    if pages_links is None:
        return print('Введите корректный запрос')
    images_links = []
    i = 1
    for page in pages_links:
        print(f'Парсинг страницы {i} из {len(pages_links)}...')
        i += 1
        html = get_html(page)
        try:
            images_links.extend(get_content(html.text))
        except TypeError:
            print('Некорректная страница')
    images = []
    try:
        post_count = int(input('Сколько постов обработать: '))
    except ValueError:
        return print('Введите корректное число')
    y = 1
    for image_link in images_links[:post_count]:  # предложить от какого и до какого?
        html = get_html(image_link)
        print(f'Обработка поста {y} из {post_count}...')
        y += 1
        images.extend(get_image(html.text))
    print(f'Постов успешно обработано: {len(images)}')
    a = 0
    try:
        b = int(input('Сколько картинок желаешь: '))
    except ValueError:
        return print('Введите корректное число')
    try:
        while a < b:
            print(choice(images))  # если сверху заменять, то тут до какого элемента
            a += 1  # либо сделать проверку на совпадение
    except IndexError:
        return print('Введите корректное число постов')
    return print('Дело сделано')


parse()
