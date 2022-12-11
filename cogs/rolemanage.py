import discord
import sqlite3
from discord.ext import commands
from config import *
import time
import math
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, help_command=None)

data_base = sqlite3.connect('bot_test.db', timeout=10)

cursor = data_base.cursor()

global payment1
global channelid
global Oplata  # Переменная в которой будет хранится оплаченная за команту сумма
global vtime

class Roles(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['магазин', 'магаз'])
    async def shop(self, ctx):
        pass
        # ----------------------------------------------------------------------
        # Я БУДУ ПЕРЕДЕЛЫВАТЬ ВСЁ В ПОКУПКЕ
        # РОЛЕЙ, МАГАЗИНЕ И ПРОЧЕМ! ВОЗМОЖНО ОБЪЕДИНЮ ПОКУПКУ ВОЙСА С ЭТИМ ДОПОЛНЕНИЕМ! ТУТ ЛУЧШЕ ОСТАВИТЬ ВСЁ
        # МЕРТВЫМ. КЛАСС КЛАССЫ COMMANDSROLE И COMMANDSVOCE НА ПЕРЕРАБОТКЕ! БУДУТ ВСЕ В ФАЙЛЕ rolemanage.py! НЕ
        # ТРОГАТЬ РАДИ ВСЕГО СВЯТОГО! ----------------------------------------------------------------------



        # @commands.command()  # создание роли
        # async def newrole(self, ctx, *, content):
        #     connection = sqlite3.connect('bot_test.db')
        #     a = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        #     oplata = 10000
        #     op = a
        #     connection.commit()
        #
        #     if op < 10000:
        #
        #         he1 = discord.Embed(title="[BuyRole]", colour=discord.Colour(0x3e038c))
        #         he1.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
        #         await ctx.send(embed=he1)
        #
        #     elif op >= 10000:
        #
        #         cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(oplata, ctx.author.id))
        #         guild = ctx.guild
        #         role = await guild.create_role(name=content)
        #         roleid = role.id
        #         await ctx.author.add_roles(role)
        #         description = f'''
        #             **Name:** <@{roleid}>
        #             **Created by:** {ctx.author.mention}
        #             '''
        #         await ctx.send("Роль была создана и выдана. Для редакции обратитесь к @St1zy3 ")
        #         print(roleid)
        #
        # @commands.command()
        # async def shop(self, ctx):
        #     he1 = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
        #     he1.add_field(name='Магазин ролей.', value="Ниже представлены роли для покупки.", inline=False)
        #     he1.add_field(name='1. [1]', value="35.000 SH", inline=False)
        #     he1.add_field(name='2. [2]', value="50.000 SH", inline=False)
        #     he1.add_field(name='Покупка.', value="Для покупки необходимо написать '/buyrole Номер роли'", inline=False)
        #     await ctx.send(embed=he1)
        #
        # @commands.command()  # Не работает выдача ролиы
        # async def buyrole(self, ctx, count: int = None):
        #     member = ctx.message.author
        #     role = discord.Role.name == '[1]'
        #     oplata = 35000
        #     role: discord.Role
        #     member: discord.Member
        #     connection = sqlite3.connect('bot_test.db')
        #     cursor = connection.cursor()
        #     balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        #     connection.commit()
        #     if count == 1:
        #         if balance >= 35000:
        #             roles = 1050283874938261544
        #             role = int(roles)
        #             await member.add_roles(roles)
        #             cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(oplata, ctx.author.id))
        #             he1 = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
        #             he1.add_field(name='Спасибо за покупку!', value="Роль была выдана.", inline=False)
        #             await ctx.send(embed=he1)
        #         else:
        #             he1 = discord.Embed(title="[Buy]", colour=discord.Colour(0x3e038c))
        #             he1.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
        #             await ctx.send(embed=he1)
        #

async def setup(bot):
    await bot.add_cog(Roles())

