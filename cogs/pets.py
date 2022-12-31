import discord
# from discord.ui import Select, View
from discord.ext import commands
from configs.config import *
import random
from logs import logger
import psycopg2 as sql
from configs.database_config import *

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

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, help_command=None)


class Pets(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=["питомцы", "кейс с питомцами", "питомец кейс"])
    async def casepets(self, ctx, move: str = None):
        moves = ["открыть", "купить", "buy", "open"]
        cursor.execute(f"SELECT pet_has FROM users WHERE id = {ctx.author.id}")
        user_pets = list(cursor.fetchone()[0])
        cursor.execute(f"SELECT casepets FROM users WHERE id = {ctx.author.id}")
        casepets = cursor.fetchone()[0]

        if move is None:

            embed = discord.Embed(title=f'[CasePets]', color=0x42f566)
            embed.add_field(name='У вас в наличии:', value=f'{casepets} кейсов с питомцами.', inline=False)
            await ctx.send(embed=embed)

        elif move is not None and move not in moves:

            emb = discord.Embed(title='[ERROR] CasePets',
                                description=f'{ctx.author.mention}, Укажите правильное действие!',
                                colour=discord.Colour(0xe73c3c))
            emb.add_field(name='Действия:', value=f'{moves}', inline=False)
            emb.add_field(name='Пример :', value='/casepets открыть')
            await ctx.send(embed=emb)

        elif move in ['окрыть', 'open']:

            cursor.execute(f"SELECT casepets FROM users WHERE id = {ctx.author.id}")
            casepets = cursor.fetchone()[0]
            val = 1
        #     if casepets >= 1:
        #         cursor.execute("UPDATE users SET casepets = casepets - {} WHERE id = {}".format(val, ctx.author.id))
        #         connection.commit()
        #         rand = random.randint(0, 50)
        #
        #         if rand == 31:
        #
        #             if wolfpets == 1:
        #                 emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
        #                 emb.add_field(name='[Итог]', value="Вам бы выпал питомец 'Волк', но он у вас уже есть.",
        #                               inline=False)
        #                 await ctx.send(embed=emb)
        #
        #             else:
        #                 cursor.execute(
        #                     "UPDATE users SET wolfpets = wolfpets + {} WHERE id = {}".format(val, ctx.author.id))
        #                 emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
        #                 emb.add_field(name='Поздравляем.', value="Вам выпал питомец 'Волк'.", inline=False)
        #                 emb.add_field(name='Питомец "Волк".',
        #                               value="Данный питомец прибавляет процент от суммы выйгрыша в казино на 7% .",
        #                               inline=False)
        #                 emb.add_field(name='Пример:".',
        #                               value="Вы сыграли в казино на 50.000 SH, победили, вам прибавляется на баланс 50.000 SH которые вы выйграли и сверху 3.500 SH за счет того что у вас данный питомец .",
        #                               inline=False)
        #                 emb.add_field(name='Посмотреть ваших питомцев:', value="/mypets", inline=False)
        #                 emb.add_field(name='Узнать информацию о всех питомцах', value="/help питомцы", inline=False)
        #                 await ctx.send(embed=emb)
        #
        #         elif rand == 14:
        #             if foxpets == 1:
        #                 emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
        #                 emb.add_field(name='[Итог]', value="Вам бы выпал питомец 'Лиса', но он у вас уже есть.",
        #                               inline=False)
        #                 await ctx.send(embed=emb)
        #
        #             else:
        #                 cursor.execute(
        #                     "UPDATE users SET foxpets = foxpets + {} WHERE id = {}".format(val, ctx.author.id))
        #                 emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
        #                 emb.add_field(name='Поздравляем.', value="Вам выпал питомец 'Лиса'.", inline=False)
        #                 emb.add_field(name='Питомец "Лиса".',
        #                               value="Данный питомец прибавляет 7% SH от времени которое вы находились в голосовом канале.",
        #                               inline=False)
        #                 emb.add_field(name='Пример:".',
        #                               value="Вы просидели в голосовом канале 4 часа, после выхода вас начислятся 4.800 SH, за счет того что у вас данный питомец , вам сверху прибавится 336 SH.",
        #                               inline=False)
        #                 emb.add_field(name='Посмотреть ваших питомцев:', value="/mypets", inline=False)
        #                 emb.add_field(name='Узнать информацию о всех питомцах', value="/help питомцы", inline=False)
        #                 await ctx.send(embed=emb)
        #
        #         elif rand == 37:
        #             if dogpets == 1:
        #                 emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
        #                 emb.add_field(name='[Итог]', value="Вам бы выпал питомец 'Собака', но он у вас уже есть.",
        #                               inline=False)
        #                 await ctx.send(embed=emb)
        #
        #             else:
        #                 cursor.execute(
        #                     "UPDATE users SET dogpets = dogpets + {} WHERE id = {}".format(val, ctx.author.id))
        #                 emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
        #                 emb.add_field(name='Поздравляем.', value="Вам выпал питомец 'Собака'.", inline=False)
        #                 emb.add_field(name='Питомец "Собака".',
        #                               value="Данный питомец возвращает вам 5 % от проигрыша в казино.",
        #                               inline=False)
        #                 emb.add_field(name='Пример:".',
        #                               value="Вы поставили в казино 5000 SH и проиграли , за счет того что у вас данный питомец, вам вернется 250 SH. :exclamation: Если ставка менее 100 SH возврата средств не будет :exclamation: ",
        #                               inline=False)
        #                 emb.add_field(name='Посмотреть ваших питомцев:', value="/mypets", inline=False)
        #                 emb.add_field(name='Узнать информацию о всех питомцах', value="/help питомцы", inline=False)
        #                 await ctx.send(embed=emb)
        #
        #
        #
        #
        #         else:
        #             emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
        #             emb.add_field(name='[Итог]', value="К сожалению вам ничего не выпало.",
        #                           inline=False)
        #             await ctx.send(embed=emb)
        #
        #     elif casepets <= 0:
        #
        #         emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
        #         emb.add_field(name='Ошибка.', value="У вас нет кейсов.", inline=False)
        #         await ctx.send(embed=emb)
        #
        # elif move in ['buy', 'купить']:
        #
        #     price = 5000  # Цена кейса
        #     val = 1  # Кол-во покупаемых кейсов.
        #     if balance < price:
        #
        #         emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
        #         emb.add_field(name='Ошибка.', value="Недостаточно средств.", inline=False)
        #         await ctx.send(embed=emb)
        #
        #     elif balance >= price:
        #
        #         cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(price, ctx.author.id))
        #         cursor.execute("UPDATE users SET casepets = casepets + {} WHERE id = {}".format(val, ctx.author.id))
        #         connection.commit()
        #         emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
        #         emb.add_field(name='Успешно.',
        #                       value="Кейс с питомцами был куплен, для открытия введите '/casepets открыть или /casepets open'.",
        #                       inline=False)
        #         await ctx.send(embed=emb)
        #
        # @commands.command(aliases=["мои питомцы", "мои петы"])
        # async def mypets(self, ctx):
        #     wolfpets = cursor.execute("SELECT wolfpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        #     foxpets = cursor.execute("SELECT foxpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        #     if wolfpets == 1 and foxpets == 0:
        #         emb = discord.Embed(title="[MyPets]", colour=discord.Colour(0x3e038c))
        #         emb.add_field(name='Ваши питомцы.', value="У вас есть только питомец 'Волк'.", inline=False)
        #         emb.add_field(name='Эффект от питомца.',
        #                       value="Данный питомец прибавляет процент от суммы выйгрыша в казино на 7%.", inline=False)
        #         await ctx.send(embed=emb)
        #     elif foxpets == 1 and wolfpets == 0:
        #         emb = discord.Embed(title="[MyPets]", colour=discord.Colour(0x3e038c))
        #         emb.add_field(name='Ваши питомцы.', value="У вас есть только питомец 'Лиса'.", inline=False)
        #         emb.add_field(name='Эффект от питомца.',
        #                       value="Данный питомец прибавляет 7% SH от времени которое вы находились в голосовом канале.",
        #                       inline=False)
        #         await ctx.send(embed=emb)
        #     elif foxpets == 1 and wolfpets == 1:
        #         emb = discord.Embed(title="[MyPets]", colour=discord.Colour(0x3e038c))
        #         emb.add_field(name='Ваши питомцы.', value="У вас есть 2 питомца, 'Волк' и 'Лиса'.", inline=False)
        #         emb.add_field(name='Эффекты от питомцев.',
        #                       value="'Волк' - Данный питомец прибавляет процент от суммы выйгрыша в казино на 7%. 'Лиса' - Данный питомец прибавляет 7% SH от времени которое вы находились в голосовом канале.",
        #                       inline=False)
        #         await ctx.send(embed=emb)
        #     elif foxpets == 0 and wolfpets == 0:
        #         emb = discord.Embed(title="[MyPets]", colour=discord.Colour(0x3e038c))
        #         emb.add_field(name='Ваши питомцы.', value="У вас нет питомцев :(", inline=False)
        #         await ctx.send(embed=emb)
        #
        # @commands.command()  # Выбрать питомца
        # async def selectpet(self, ctx):
        #     select = Select(
        #
        #         options=[
        #             discord.SelectOption(
        #                 label="Wolf",
        #                 emoji="🐺"
        #             ),
        #
        #             discord.SelectOption(
        #                 label="Fox",
        #                 emoji="🦊"
        #             ),
        #
        #             discord.SelectOption(
        #                 label="Dog",
        #                 emoji="🐶"
        #             )
        #         ])
        #
        #     async def my_callback(interaction):  # Если namepet active - выбран данный питомец
        #         val = 1
        #         wolfpet = cursor.execute("SELECT wolfpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        #         foxpet = cursor.execute("SELECT foxpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        #         dogpet = cursor.execute("SELECT dogpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        #         wolfactive = \
        #         cursor.execute("SELECT wolfactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
        #             0]
        #         foxactive = \
        #         cursor.execute("SELECT foxactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        #         dogactive = \
        #         cursor.execute("SELECT dogactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        #         connection = data_base
        #         if select.values[0] == "Wolf":
        #             if wolfpet == 0:
        #                 await ctx.send("У вас нет данного питомца.")
        #             else:
        #                 if wolfactive == 1:
        #                     await ctx.send("У вас установлен данный питомец.")
        #                 elif wolfactive == 0 and foxactive == 0 and dogactive == 0:
        #                     cursor.execute(
        #                         "UPDATE users SET wolfactive = wolfactive + {} WHERE id = {}".format(val,
        #                                                                                              ctx.author.id))
        #                     connection.commit()
        #                 elif wolfactive == 0 and foxactive >= 1 and dogactive >= 1:
        #                     await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
        #                     cursor.execute(
        #                         "UPDATE users SET wolfactive = wolfactive + {} WHERE id = {}".format(val,
        #                                                                                              ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET foxactive = foxactive - {} WHERE id = {}".format(val, ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET dogactive = dogactive - {} WHERE id = {}".format(val, ctx.author.id))
        #
        #                     connection.commit()
        #                 elif wolfactive == 0 and foxactive >= 1 and dogactive == 0:
        #                     await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
        #                     cursor.execute(
        #                         "UPDATE users SET wolfactive = wolfactive + {} WHERE id = {}".format(val,
        #                                                                                              ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET foxactive = foxactive - {} WHERE id = {}".format(val, ctx.author.id))
        #
        #                     connection.commit()
        #                 elif wolfactive == 0 and foxactive == 0 and dogactive >= 1:
        #                     await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
        #                     cursor.execute(
        #                         "UPDATE users SET wolfactive = wolfactive + {} WHERE id = {}".format(val,
        #                                                                                              ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET dogactive = dogactive - {} WHERE id = {}".format(val, ctx.author.id))
        #
        #                     connection.commit()
        #
        #         elif select.values[0] == "Fox":
        #             if foxpet == 0:
        #                 await ctx.send("У вас нет данного питомца.")
        #             else:
        #                 if foxactive == 1:
        #                     await ctx.send("У вас установлен данный питомец.")
        #                 elif wolfactive == 0 and foxactive == 0 and dogactive == 0:
        #                     await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
        #                     cursor.execute(
        #                         "UPDATE users SET foxactive = foxactive + {} WHERE id = {}".format(val, ctx.author.id))
        #                     connection.commit()
        #                 elif wolfactive >= 1 and foxactive == 0 and dogactive >= 1:
        #                     await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
        #                     cursor.execute(
        #                         "UPDATE users SET foxactive = foxactive + {} WHERE id = {}".format(val, ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET wolfactive = wolfactive - {} WHERE id = {}".format(val,
        #                                                                                              ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET dogactive = dogactive - {} WHERE id = {}".format(val, ctx.author.id))
        #                     connection.commit()
        #                 elif wolfactive >= 0 and foxactive == 0 and dogactive == 0:
        #                     await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
        #                     cursor.execute(
        #                         "UPDATE users SET foxactive = foxactive + {} WHERE id = {}".format(val, ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET wolfactive = wolfactive - {} WHERE id = {}".format(val,
        #                                                                                              ctx.author.id))
        #                     connection.commit()
        #                 elif wolfactive >= 0 and foxactive == 0 and dogactive >= 1:
        #                     await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
        #                     cursor.execute(
        #                         "UPDATE users SET foxactive = foxactive + {} WHERE id = {}".format(val, ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET dogactive = dogactive - {} WHERE id = {}".format(val, ctx.author.id))
        #
        #                     connection.commit()
        #
        #         elif select.values[0] == "Dog":
        #             if dogpet == 0:
        #                 await ctx.send("У вас нет данного питомца.")
        #             else:
        #                 if dogactive == 1:
        #                     await ctx.send("У вас установлен данный питомец.")
        #                 elif wolfactive == 0 and foxactive == 0 and dogactive == 0:
        #                     await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
        #                     cursor.execute(
        #                         "UPDATE users SET dogactive = dogactive + {} WHERE id = {}".format(val, ctx.author.id))
        #                     connection.commit()
        #                 elif wolfactive == 1 and foxactive == 1 and dogactive == 0:
        #                     await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
        #                     cursor.execute(
        #                         "UPDATE users SET wolfactive = wolfactive - {} WHERE id = {}".format(val,
        #                                                                                              ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET foxactive = foxactive - {} WHERE id = {}".format(val, ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET dogactive = dogactive + {} WHERE id = {}".format(val, ctx.author.id))
        #                     connection.commit()
        #                 elif dogactive == 0 and wolfactive >= 1 and foxactive == 0:
        #                     await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
        #                     cursor.execute(
        #                         "UPDATE users SET wolfactive = wolfactive - {} WHERE id = {}".format(val,
        #                                                                                              ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET dogactive = dogactive + {} WHERE id = {}".format(val, ctx.author.id))
        #                     connection.commit()
        #                 elif dogactive == 0 and wolfactive == 0 and foxactive >= 1:
        #                     await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
        #                     cursor.execute(
        #                         "UPDATE users SET foxactive = foxactive - {} WHERE id = {}".format(val, ctx.author.id))
        #                     cursor.execute(
        #                         "UPDATE users SET dogactive = dogactive + {} WHERE id = {}".format(val, ctx.author.id))
        #                     connection.commit()
        #
        #     select.callback = my_callback
        #     view = View()
        #     view.add_item(select)
        #     await ctx.send("Select Pet", view=view)


async def setup(bot):
    await bot.add_cog(Pets())
#
