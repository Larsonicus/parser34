import random
import discord
from discord.ext import commands
import os
import logging
import requests
from bs4 import BeautifulSoup

# emoji = []


game = ["камень", "ножницы", "бумага"]

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4414.0 '
                         'Safari/537.36 Edg/90.0.803.0', 'accept': '*/*'}
HOST = 'https://rule34.xxx/'

log_channel = 710931680701186110  # 818119479589470259
xxx_channel = 710931680701186110  # 818128708439244821

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="$", case_insensitive=True)


@bot.event
async def on_ready():
    print(f'{bot.user.name} готов к работе.')


@bot.event
async def on_command_error(ctx, error):
    print(f'В собщении от {ctx.author}: "{ctx.message.content}" Ошибка: {error}')  # вывод ошибки

    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(f'Данной команды не существует, {ctx.author.mention}.')
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send(f'Ты бесправное животное {ctx.author.mention}.')


@bot.event
async def on_message(message):
    if not message.author.bot:
        if message.content.lower() in ["нет", "net", "ytn"]:
            await message.channel.send(f'Пидора ответ! Ха-ха {message.author.mention}.')
        if message.content.lower() in ["da", "да", "lf", "d4"]:
            await message.channel.send(f'Манда! Ахахахах {message.author.mention}.')
        if message.content.startswith("$"):
            await bot.process_commands(message)
        '''if not message.content.startswith("$"):  # реакция на сообщение
            await message.add_reaction(message.guild.emojis[random.randint(0, len(message.guild.emojis) - 1)])'''


@bot.event
async def on_message_delete(message):  # также добавить, когда юзер изменяет сообщение
    if not message.author.bot:
        if not message.content.startswith("$"):
            if not message.content == "":
                await message.channel.send(f'Пользователь {message.author.mention} удалил сообщение:')
                await message.channel.send(f'>>> {message.content}')


@bot.command(help="Это пинг, отвечает понг")
async def ping(ctx):
    if ctx.message.content.startswith("$пинг") or ctx.message.content.startswith("$Пинг") \
            or ctx.message.content.startswith("$ПИНГ"):
        await ctx.send(f"Понг! {ctx.author.mention}")
    elif ctx.message.content.startswith("$ping") or ctx.message.content.startswith("$Ping") \
            or ctx.message.content.startswith("$PING"):
        await ctx.send(f"Pong! {ctx.author.mention}")


@bot.command(name="камень", help="Выбросить камень")
async def rock(ctx):
    a = game[random.randint(0, 2)]
    await ctx.send(f"Я выбросил {a}.")
    if a == "камень":
        await ctx.send(f"Ничья! {ctx.author.mention}.")
    elif a == "ножницы":
        await ctx.send(f"Ты выиграл! {ctx.author.mention}.")
    elif a == "бумага":
        await ctx.send(f"Ты проиграл! Лох {ctx.author.mention}.")


@bot.command(name="ножницы", help="Выбросить ножницы")
async def scissors(ctx):
    a = game[random.randint(0, 2)]
    await ctx.send(f"Я выбросил {a}.")
    if a == "ножницы":
        await ctx.send(f"Ничья! {ctx.author.mention}.")
    if a == "бумага":
        await ctx.send(f"Ты выиграл! {ctx.author.mention}.")
    if a == "камень":
        await ctx.send(f"Ты проиграл! {ctx.author.mention}.")


@bot.command(name="бумага", help="Выбросить бумагу")
async def paper(ctx):
    a = game[random.randint(0, 2)]
    await ctx.send(f"Я выбросил {a}.")
    if a == "бумага":
        await ctx.send(f"Ничья! {ctx.author.mention}.")
    if a == "камень":
        await ctx.send(f"Ты выиграл! {ctx.author.mention}.")
    if a == "ножницы":
        await ctx.send(f"Ты проиграл! {ctx.author.mention}.")


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
    try:
        for i in items:
            image.append(i.find('img', alt_='').get('src'))
    except AttributeError:
        videos = soup.find_all('source')
        for video in videos:
            image.append(video.get('src'))
    return image


@bot.command(name="фулл", aliases=['full'], help="Скидывает фулл", pass_context=True)
async def parse(ctx, *tag):
    tag = ''.join(tag)
    blacklist = '+-gay+-futanari+-1futa+-2futas+-3futas+-solo_male+-male_only+-trap+-femboy+-fat+-bbw'
    global url
    url = f'https://rule34.xxx/index.php?page=post&s=list&tags={tag}{blacklist}'
    html = get_html(url)
    pages_links = get_pages_count(html.text)
    if pages_links is None:
        return await ctx.send('Введите корректный запрос')
    images_links = []
    pages = []
    for page in pages_links:
        pages.append(page)
    html = get_html(random.choice(pages))
    try:
        images_links.extend(get_content(html.text))
    except TypeError:
        print('Обнаружена некорректная страница')
    try:
        image_link = random.choice(images_links)
    except IndexError:
        return await ctx.send('Не важно')
    html = get_html(image_link)
    images = []
    images.extend(get_image(html.text))
    await ctx.send((random.choice(images)))  # если сверху заменять, то тут до какого элемента


bot.run(os.environ.get("BOT_TOKEN"))
