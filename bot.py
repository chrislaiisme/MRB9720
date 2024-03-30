LOCAL = 0
TOKEN = "hidden"

import discord
import math
import time
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from datetime import datetime
from datetime import timezone

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix = "$", intents = intents)

prefix = ["dc_bot/", ""]
time_shift = [28800, 0]

explode = []
f = open(prefix[LOCAL] + "explode.txt", "r", encoding="utf-8")
i = 0
for line in f.read().splitlines():
    explode.append(Choice(name = line, value = i))
    i = i+1
f.close()

miserable = []
f = open(prefix[LOCAL] + "miserable.txt", "r", encoding="utf-8")
for line in f.read().splitlines():
    miserable.append(line)
f.close()

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f">> {bot.user} << 上線中")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    ''' ========== condemn function ========== '''
    s = message.content.lower()
    bln = False
    for i in miserable:
        if s.find(i) != -1:
            bln = True
            break
    if bln == True:
        await message.channel.send("好了啦你超可悲")

    ''' ========== but you know what? your mom died ========== '''
    s = message.content
    if len(s)>=6 and s.find("但是你知道嗎") == len(s)-6:
        await message.channel.send("你媽死了")

''' ========== record command ========== '''
@bot.tree.command(name = "record", description = "來看看又是誰在那邊亂講話了")
@app_commands.describe(word = "他在公三小", person = "誰講的", time_past = "大概幾秒前講的")
@app_commands.choices(person = explode)
async def record(interaction: discord.Interaction, word: str, person: Choice[int], time_past: int):
    stamp = math.floor(time.time())
    stamp -= time_past;

    stamp += time_shift[LOCAL]

    tm = datetime.fromtimestamp(stamp)
    date_time = tm.strftime("%Y/%m/%d %H:%M:%S")
    await interaction.response.send_message(word + ' --- ' + person.name + ' ' + date_time)

''' ========== condemn command ========== '''
@bot.tree.command(name = "condemn", description = "來譴責一些亂講話的人")
@app_commands.describe(person = "誰講的")
@app_commands.choices(person = explode)
async def record(interaction: discord.Interaction, person: Choice[int]):
    await interaction.response.send_message(person.name + ' 你超可悲')

bot.run(TOKEN)