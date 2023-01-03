import discord
from discord.ext import commands
from configs.config import *
import datetime
import asyncio
import math
import os
from logs import logger, handler
import psycopg2 as sql
from configs.database_config import *


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, help_command=None)

# global payment1
global channelid
global Oplata  # Переменная в которой будет хранится оплаченная за команту сумма
global vtime

data_base = sql.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port,

    )
data_base.autocommit = False

try:

    cursor = data_base.cursor()


except Exception as _ex:

    logger.info(f'Error happend while connecting to Database! {_ex}')


# bot.event
@bot.event
async def on_ready():
    logger.info("Bot started")
    logger.info(f"Bot name is {bot.user.name}")
    logger.info(f'Client id is {bot.user.id}')
    global tdict
    tdict = {}
    # await bot.add_cog(CommandsVoice())
    await bot.add_cog(CommandsRoles())
    await bot.change_presence(activity=discord.Game('/help'))
    for guild in bot.guilds:

        logger.info(f'Connected to server, id is: {guild.id}')

        for member in guild.members:

            cursor.execute(f"SELECT id FROM users where id={member.id}")

            if cursor.fetchone() is None:

                cursor.execute(
                    f"INSERT INTO users (id, nickname, mention, money) VALUES ({member.id}, '{member.name}', '<@{member.id}>', 0)")
                data_base.commit()
                logger.info(f'Added user to database')

            else:

                pass
            logger.info('Database Full')
    for filename in os.listdir("./cogs"):  # перебирает все файлы в выбранной папке
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")  # загрузка КОГов в основной файл
            logger.info(f'Extension {filename} loaded')


@bot.event
async def on_ready():

    await asyncio.sleep(60)
    timestamp = datetime.datetime.now()
    cursor.execute(f'SELECT (id, last_payment, account) FROM channels WHERE {timestamp} - last_payment = 0')
    row = cursor.fetchall()
    week_cost = 12_000

    for voice in row:

        if voice[2] < week_cost:

            channel = bot.get_channel(voice[0])
            await channel.delete()
            cursor.execute(f'DELETE FROM channels WHERE id = {voice[0]}')
            data_base.commit()

        else:

            cursor.execute(f'UPDATE channels SET account = account - {week_cost} WHERE id = {voice[0]}')
            cursor.execute(f'UPDATE channels SET last_payment = {timestamp} WHERE id = {voice[0]}')
            data_base.commit()


@bot.command()
async def plugin(ctx, todo: str = None):
    todos = ['-l', '-r', '-u']

    if todo is None:

        for filename in os.listdir("./cogs"):  # перебирает все файлы в выбранной папке

            if filename.endswith(".py"):
                await ctx.send(f'Плагин - {filename[:-3]} существует!')

        await ctx.send('/plugin -l чтобы загрузить')

    if todo is not None and todo not in todos:

        emb = discord.Embed(title='[ERROR] plugin', description=f'{ctx.author.mention}, Укажите приемлемое действие',
                            colour=discord.Colour(0xe73c3c))
        emb.add_field(name='Действия:', value='-r - restart, -l - load, -u - unload', inline=False)
        emb.add_field(name='Пример :', value='/plugin -r')
        await ctx.send(embed=emb)

    elif todo == '-l':

        for filename in os.listdir("./cogs"):  # перебирает все файлы в выбранной папке

            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")  # загрузка КОГов в основной файл
                logger.info('Loaded plugins')
        await ctx.send('Plugins loaded')

    elif todo == '-u':

        for filename in os.listdir("./cogs"):

            if filename.endswith(".py"):
                await bot.unload_extension(f"cogs.{filename[:-3]}")

        await ctx.send('Plugins unloaded')
        logger.info('Plugins unloaded')

    elif todo == '-r':

        for filename in os.listdir("./cogs"):

            if filename.endswith(".py"):
                await bot.reload_extension(f"cogs.{filename[:-3]}")
        logger.info("plugins reloaded")
        await ctx.send('Plugins reloaded')


class CommandsRoles(commands.Cog):
    def __init__(self):
        self.bot = bot

    @commands.command()  # создание роли
    async def newrole(self, ctx, *, content):
        cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id))
        a = cursor.fetchone()[0]
        oplata = 10000
        op = a
        data_base.commit()

        if op < 10000:

            he1 = discord.Embed(title="[BuyRole]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
            await ctx.send(embed=he1)

        elif op >= 10000:

            cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(oplata, ctx.author.id))
            guild = ctx.guild
            role = await guild.create_role(name=content)
            roleid = role.id
            await ctx.author.add_roles(role)
            description = f'''
            **Name:** <@{roleid}>
            **Created by:** {ctx.author.mention}
            '''
            await ctx.send("Роль была создана и выдана. Для редакции обратитесь к @St1zy3 ")
            print(roleid)

    @commands.command()
    async def shop(self, ctx):
        he1 = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
        he1.add_field(name='Магазин ролей.', value="Ниже представлены роли для покупки.", inline=False)
        he1.add_field(name='1. [1]', value="35.000 SH", inline=False)
        he1.add_field(name='2. [2]', value="50.000 SH", inline=False)
        he1.add_field(name='Покупка.', value="Для покупки необходимо написать '/buyrole Номер роли'", inline=False)
        await ctx.send(embed=he1)

    @commands.command()  # Не работает выдача роли
    async def buyrole(self, ctx, count: int = None):
        member = ctx.message.author
        role = discord.Role.name == '[1]'
        oplata = 35000
        role: discord.Role
        member: discord.Member
        cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id))
        balance = cursor.fetchone()[0]
        data_base.commit()

        if count == 1:

            if balance >= 35000:

                roles = 1050283874938261544
                await member.add_roles(roles)
                cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(oplata, ctx.author.id))
                he1 = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Спасибо за покупку!', value="Роль была выдана.", inline=False)
                await ctx.send(embed=he1)

            else:

                he1 = discord.Embed(title="[Buy]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
                await ctx.send(embed=he1)


bot.run(settings['token'], log_handler=handler)
