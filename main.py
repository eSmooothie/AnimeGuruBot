# imports
import discord
import os
import random
import requests
import json
import asyncio
from keep_alive import keep_alive
import anime
from replit import db
import time_func
from discord.ext import tasks, commands

client = discord.Client() # create an instance of a client. This is the connection to discord

TOKEN = os.getenv('TOKEN')

ALL_CHANNELS = {}

class Anime:
  def __init__(self, title):
    self.title = title

@client.event # this used to register an event.
# this is an asynchronous lib, so things are done with callbacks
# callbacks is a function that is called when something else happens.
# the on_ready() event is called when the bot is ready to start being used.
async def on_ready():
  # delete_all_keys() # delete all generated keys
  # print(client.get_all_channels())
  for ch in client.get_all_channels():
    ALL_CHANNELS[ch.name] = ch.id
  print("We have logged in as {0.user}".format(client))

@client.event 
# when bot recieve message, the on_message() event is called.
async def on_message(message):
    anime_channel = client.get_channel(ALL_CHANNELS['anime-suggestions'])
    ERR_MSG = "Sorry Im not allowed to showcase my capabilities here. Go to {}.".format(anime_channel.mention)
    
    if message.author == client.user:
      return

    msg = message.content

    if msg.startswith(';inspire'):
      print(message.author)
      quote = get_quote()
      await message.channel.send("{0.mention}, I hope you will be inspired by this quote.```{1}```".format(message.author,quote))
      return

    if msg.startswith(';clean'):
      amount = 20
      await message.channel.send("Cleaning...")
      await asyncio.sleep(2)
      await message.channel.purge(limit=amount)
      return

    if msg.startswith(';cmd') and message.channel.id == ALL_CHANNELS['anime-suggestions']:
      await message.channel.send(display_bot_commands()) # display all bot command
    elif msg.startswith(';cmd'):
      # if another channel
      msg = "I can only perform `;clean` and `;inspire` command here. :pensive: Go to {}, to witness my full potential.".format(anime_channel.mention)
      await message.channel.send(msg)
      return

    
    if msg.startswith(';add'):
      if message.channel.id == ALL_CHANNELS['anime-suggestions']:
        user_msg = msg.split(' ')
        anime_title = user_msg[1:]
        anime_title = ' '.join(anime_title)
        new_anime = Anime(anime_title)
        add_anime(new_anime)

        await message.channel.send("{} added in database.".format(anime_title)) 
      else:
        await message.channel.send(ERR_MSG)
        return

    if msg.startswith(';list'):
      if message.channel.id == ALL_CHANNELS['anime-suggestions']:
        user_msg = msg.split(' ')
        if len(user_msg) < 2:
          page = 1
        else:
          page = int(user_msg[1])

        await message.channel.send(show_anime_list(page))
      else:
        await message.channel.send(ERR_MSG)
        return

    if msg.startswith(';suggest'):
      if message.channel.id == ALL_CHANNELS['anime-suggestions']:
        await message.channel.send(suggest_anime())
      else:
        await message.channel.send(ERR_MSG)
        return

    # search anime
    await search_anime(msg, message, ERR_MSG)
    # pagination
    await pagination(msg, message)

async def search_anime(cmd, message, err_msg):
  if cmd.startswith(';anime_search') or cmd.startswith(';search'):
    if message.channel.id == ALL_CHANNELS['anime-suggestions']:
      keyword = cmd.split(' ')
      if len(keyword) < 2:
        await message.channel.send("Invalid parameter. `;anime_search <keyword>`")
        return
      
      data = anime.filter_text(keyword[1])
      db['pagination'] = data['links']
      db['curr_page'] = 1
      alist = anime.get_anime_list(data)
      count = anime.get_total_result(data)
      db['last_page'] = count//3
      await message.channel.send("Total Result Found: {}".format(count))
      await message.channel.send("Page: {}".format(db['curr_page']))
      for animeData in alist:
        await message.channel.send(animeData)
    else:
      await message.channel.send(err_msg)

async def pagination(cmd,message):
  if cmd.startswith(';first_page'):
    data = anime.first_page(db['pagination'])
    db['pagination'] = data['links']
    
    alist = anime.get_anime_list(data)
    await message.channel.purge(limit=5)

    db['curr_page'] = 1
    await message.channel.send("Page: {}".format(db['curr_page']))
    for animeData in alist:
      await message.channel.send(animeData)

  if cmd.startswith(';last_page'):
    data = anime.last_page(db['pagination'])
    db['pagination'] = data['links']
    
    alist = anime.get_anime_list(data)
    await message.channel.purge(limit=5)

    await message.channel.send("Page: {}".format(db['last_page']))
    for animeData in alist:
      await message.channel.send(animeData)

  if cmd.startswith(';next_page'):
    data = anime.next_page(db['pagination'])
    db['pagination'] = data['links']
    
    alist = anime.get_anime_list(data)
    await message.channel.purge(limit=5)

    db['curr_page'] = db['curr_page'] + 1
    await message.channel.send("Page: {}".format(db['curr_page']))

    for animeData in alist:
      await message.channel.send(animeData)

  if cmd.startswith(';prev_page'):
    data = anime.prev_page(db['pagination'])
    db['pagination'] = data['links']
    
    alist = anime.get_anime_list(data)
    await message.channel.purge(limit=5)

    db['curr_page'] -= 1
    await message.channel.send("Page: {}".format(db['curr_page']))
    for animeData in alist:
      await message.channel.send(animeData)


@tasks.loop(hours = 1.0) #loops every x hour 
async def display_inspire_quotes():
  current_time = time_func.getCurrentTime()
  quote = get_quote()
  ch1 = client.get_channel(ALL_CHANNELS['general'])
  # ch2 = client.get_channel(ALL_CHANNELS['losers-streak'])
  
  if current_time.hour == time_func.MORNING_QUOTE_TIME:
    await ch1.send("Morning Quote ```{}```".format(quote))
    # await ch2.send("Morning Quote ```{}```".format(quote))

  elif current_time.hour == time_func.AFTERNOON_QUOTE_TIME:
    await ch1.send("Afternoon Quote ```{}```".format(quote))
    # await ch2.send("Afternoon Quote ```{}```".format(quote))
  elif current_time.hour == time_func.EVENING_QUOTE_TIME:
    await ch1.send("Evening Quote ```{}```".format(quote))
    # await ch2.send("Evening Quote ```{}```".format(quote))
  
@display_inspire_quotes.before_loop
async def before_display_inspire_quotes():
  print('waiting...')
  await client.wait_until_ready()

def display_bot_commands():
    return """
Commands List
`;cmd - display all available commands`
`;add <title> - add new anime in the list: `
`;list <page no.> - display 10 anime in the list`
`;suggest - get suggestion`
`;clean - clean channel messages`
`;inspire - get random inspiring quote`
`;search <keyword>,;anime_search <keyword> - display list of anime`
~~`;cat/;category [<genre>,<genre>,...,<genre>] - display list of anime based on search categories`~~ `soon`
Pagination
`;next_page`,`;prev_page`,`;last_page`, and `;first_page`
    """

# add anime in db
def add_anime(data): 
  key = hash(data.title.lower())
  db[key] = {"title":data.title,"genre": [],"detail":"None"}

# show list of anime
def show_anime_list(page): 
  matches = db.keys()
  matches = list(matches)
  # 10 anime per page
  end = page * 10
  start = end - 10
  anime_list = "Page {}```".format(page)
  for i in range(start, end):
    if i >= len(matches):
      anime_list = anime_list + "{end}"
      break
    key = matches[i]
    # print("{}. {}".format(i+1, key))
    anime = db[key]
    anime_list = anime_list + "{}. {}\n".format(i+1, anime["title"])
  anime_list = anime_list + "```"
  return anime_list

# choice an anime in the list then return it
def suggest_anime():
  matches = db.keys()
  matches = list(matches)
  key = random.choice(matches)
  anime = db[key]
  return "My suggestion is `{}`. :smiling_face_with_3_hearts:".format(anime["title"])

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = "" + json_data[0]["q"] + "\n- " + json_data[0]["a"]
  return(quote)

# delete all keys
def delete_all_keys():
  for keys in db.keys():
    del db[keys]


keep_alive()
display_inspire_quotes.start()
client.run(TOKEN)


