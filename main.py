# imports
import discord
import os
import random
import asyncio
from keep_alive import keep_alive
from replit import db

class Anime:
  def __init__(self,title, genre, details):
    self.title = title
    self.genre = genre
    self.details = details

client = discord.Client() # create an instance of a client. This is the connection to discord

TOKEN = os.getenv('TOKEN')

CHANNEL_ID = 849276031684575282

message_obj = []

@client.event # this used to register an event.
# this is an asynchronous lib, so things are done with callbacks
# callbacks is a function that is called when something else happens.
# the on_ready() event is called when the bot is ready to start being used.
async def on_ready():
  # delete_all_keys() # delete all generated keys
  print("We have logged in as {0.user}".format(client))


@client.event 
# when bot recieve message, the on_message() event is called.
async def on_message(message):
    if message.author == client.user:
      return

    # if message.channel.id != CHANNEL_ID:
    #   anime_channel = client.get_channel(CHANNEL_ID)
    #   msg = "Sorry Im not allowed to talk here. Go to {}.".format(anime_channel.mention)
    #   obj = await message.channel.send(msg)
    #   message_obj.append(obj)
    #   return

    if message.content.startswith(';cmd'):
      await message.channel.send(display_bot_commands()) # display all bot command

    if message.content.startswith(';add'):
      user_msg = message.content.split(' ')
      anime_title = user_msg[1:]
      anime_title = ' '.join(anime_title)
      new_anime = Anime(anime_title, None, None)
      add_anime(new_anime)
      await message.channel.send("{} added in database.".format(anime_title)) # display message in discord


    if message.content.startswith(';list'):
      user_msg = message.content.split(' ')
      if len(user_msg) < 2:
        page = 1
      else:
        page = int(user_msg[1])

      await message.channel.send(show_anime_list(page))


    if message.content.startswith(';suggest'):
      await message.channel.send(suggest_anime())

    if message.content.startswith(';clean'):
      amount = 20
      await message.channel.send("Cleaning...")
      await asyncio.sleep(2)
      await message.channel.purge(limit=amount)

def display_bot_commands():
    return """
Commands List
`;cmd - display all available commands`\n
`;add <title> - add new anime in the list: `\n
`;list <page no.> - display 10 anime in the list`\n
`;suggest - get suggestion`\n
`;clean - clean channel messages`
    """

# add anime in db
def add_anime(data): 
  key = hash(data)
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

# delete all keys
def delete_all_keys():
  for keys in db.keys():
    del db[keys]


keep_alive()
client.run(TOKEN)


