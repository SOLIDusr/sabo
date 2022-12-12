import discord
import sqlite3
from discord.ext import commands
from config import *
from discord.ui import Button, View
from config_dicts import *

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, help_command=None)

data_base = sqlite3.connect('bot_test.db', timeout=10)

cursor = data_base.cursor()

global payment1
global channelid
global Oplata  # Переменная в которой будет хранится оплаченная за команту сумма
global vtime


class Shop(commands.Cog):

    def __init__(self):
        self.bot = bot

    # Команда для создания роли

    @commands.command()
    async def role(self, ctx, content):
        oplata = 10000
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

    # Команда для меню магазина

    @commands.command(aliases=['магазин', 'магаз'])
    async def shop(self, ctx):

        # Проверка на возможность выдать роль

        async def roles():

            connection = sqlite3.connect('bot_test.db')
            a = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            op = a
            connection.commit()

            if op < 10000:

                embd = discord.Embed(title="[BuyRole]", colour=discord.Colour(0x3e038c))
                embd.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
                await ctx.send(embed=embd)

            elif op >= 10000:
                embd = discord.Embed(title="[BuyRole]", colour=discord.Colour(0x3e038c))
                embd.add_field(name='Вам доступна покупка уникальной роли.', value="Введите /role [название], чтобы "
                                                                                   "приобрести роль.!", inline=False)
                await ctx.send(embed=embd)

        async def existing_role():
            emb = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Магазин ролей.', value="Ниже представлены роли для покупки.", inline=False)
            for item in shop.keys():
                emb.add_field(name=f'Роль - {item}. Стоимость: {shop[item]}')
            emb.add_field(name='Покупка.', value="Для покупки необходимо написать '/buyrole Номер роли'", inline=False)
            await ctx.send(embed=emb)

        # Проверка на покупку войса

        async def rooms():
            pass

        # Само по себе меню магазина

        emb = discord.Embed(title='[SHOP]', description="Тут вы можете совцершать покупки через систему виртуальной "
                                                        "валюты.", colour=discord.Colour.purple())
        emb.add_field(name='Shop', value='Все категории представлены ниже', inline=False)
        roles_b = Button(label='Досупные роли', style=discord.ButtonStyle.primary, emoji='👑')
        custom_role_b = Button(label='Личная роль', style=discord.ButtonStyle.primary,
                               emoji='<:booster:1029482318118797412>')
        room_b = Button(label='Личная комната', style=discord.ButtonStyle.primary, emoji='🔊')

        # Ответы от нажатий кнопок

        async def role_call(inter):
            await inter.response.defer()
            await roles()

        async def room_call(inter):
            await inter.response.defer()
            await rooms()

        async def buyrole_call(inter):
            await inter.response.defer()
            await existing_role()

        custom_role_b.callback = role_call
        room_b.callback = room_call
        roles_b.callback = buyrole_call
        view = View()
        view.add_item(custom_role_b)
        view.add_item(room_b)
        await ctx.send(embed=emb, view=view)

        # @commands.command()  # создание роли
        #
        # @commands.command()
        # async def shop(self, ctx):
        #     emb = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
        #     emb.add_field(name='Магазин ролей.', value="Ниже представлены роли для покупки.", inline=False)
        #     emb.add_field(name='1. [1]', value="35.000 SH", inline=False)
        #     emb.add_field(name='2. [2]', value="50.000 SH", inline=False)
        #     emb.add_field(name='Покупка.', value="Для покупки необходимо написать '/buyrole Номер роли'", inline=False)
        #     await ctx.send(embed=emb)
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
        #             emb = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
        #             emb.add_field(name='Спасибо за покупку!', value="Роль была выдана.", inline=False)
        #             await ctx.send(embed=emb)
        #         else:
        #             emb = discord.Embed(title="[Buy]", colour=discord.Colour(0x3e038c))
        #             emb.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
        #             await ctx.send(embed=emb)
        #


async def setup(bot):
    await bot.add_cog(Shop())
