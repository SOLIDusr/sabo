import discord
<<<<<<< Updated upstream
import sqlite3
=======
>>>>>>> Stashed changes
from discord.ui import Select, View
from discord.ext import commands
from configs.config import *
import random
import math
<<<<<<< Updated upstream

data_base = sqlite3.connect('bot_test.db', timeout=10)
cursor = data_base.cursor()

# the goad to get rid of globals
=======
from main import cursor, data_base, bot


# the goal to get rid of globals
>>>>>>> Stashed changes
global payment1
global channelid
# global Oplata  # Переменная в которой будет хранится оплаченная за команту сумма (Not used(strange))
global vtime

<<<<<<< Updated upstream
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)


class Gambling(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['Казино', 'казино', 'casino', 'Casino'])
    async def __casino(self, ctx, amount: int = None):
        balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        connection = data_base
        number = random.randint(1, 100)
        jackpot = amount * 5

        # Условия и т.д

        if amount is None:

            emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
            emb.add_field(name='[Ошибка]', value="Вы забыли указать ставку!", inline=False)
            await ctx.send(embed=emb)

        elif amount > balance or amount < 0:

            emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
            emb.add_field(name='[Ошибка]', value="Недостаточно средств.", inline=False)
            await ctx.send(embed=emb)

        elif balance <= 0:

            emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
            emb.add_field(name='[Ошибка]', value="Недостаточно средств.", inline=False)
            await ctx.send(embed=emb)

        else:

            if number < 50:
                dogavtive = cursor.execute("SELECT dogactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
                    0]
                if dogavtive == 1:
                    if amount <= 100:
                        cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
                        connection.commit()
                        embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                        embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
                        await ctx.send(embed=embed)
                    else:
                        dogeffect = 5 * (1/100) * amount
                        roundup = math.ceil(dogeffect)
                        cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
                        cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(roundup, ctx.author.id))
                        connection.commit()
                        embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                        embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
                        embed.add_field(name='За счет того что у вас есть питомец собака, вам вернули', value=f'{roundup} SH', inline=False)
                        await ctx.send(embed=embed)
                else:  
                    cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
                    connection.commit()
                    embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                    embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
                    await ctx.send(embed=embed)

            elif number == 93:
                wolfactive = cursor.execute("SELECT wlofactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
                    0]
                if wolfactive == 1:
                    wolfeffect = 7 * (1 / 100) * jackpot
                    roundup = math.ceil(wolfeffect)  # Округление
                    result = jackpot + roundup
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(result, ctx.author.id))
                    embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                    embed.add_field(name='О боже мой!!! Вы выйграли JACKPOT, мы добавили вам на баланс:',
                                    value=f'{jackpot} SH + Бонус: {roundup} SH за счет того что у вас есть питомец "Волк".',
                                    inline=False)
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                    embed.add_field(name='О боже мой!!! Вы выйграли JACKPOT, мы добавили вам на баланс:',
                                    value=f'{jackpot} SH', inline=False)
                    await ctx.send(embed=embed)

            elif number == 27:

                emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='[Итог]', value="Вам попалось SAFE-ЯЧЕЙКА, вы не потеряли свой баланс.",
                              inline=False)
                await ctx.send(embed=emb)

            elif number == 13:

                emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='[Итог]', value="Вам попалось SAFE-ЯЧЕЙКА, вы не потеряли свой баланс.",
                              inline=False)
                await ctx.send(embed=emb)

            else:
                wolfactive = cursor.execute("SELECT wolfactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
                    0]
                if wolfactive == 1:

                    wolfeffect = 7 * (1 / 100) * amount
                    roundup = math.ceil(wolfeffect)
                    result = amount + roundup
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(result, ctx.author.id))
                    connection.commit()
                    embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                    embed.add_field(name='Поздравляю! Вы выйграли:',
                                    value=f'{amount} SH + Бонус: {roundup} SH за счет того что у вас есть питомец "Волк".',
                                    inline=False)
                    await ctx.send(embed=embed)

                else:
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(amount, ctx.author.id))
                    connection.commit()
                    embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                    embed.add_field(name='Поздравляю! Вы выйграли:', value=f'{amount} SH', inline=False)
                    await ctx.send(embed=embed)

    @commands.command()
    async def roulette(self, ctx, amount: int = None, count: int = None):
        connection = data_base
        number = random.randint(0, 36)
        balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]

        if amount is None:

            await ctx.send("Вы забыли указать ставку!")

        elif count is None:

            await ctx.send("Нужно выбрать на что ставить.")

        elif count > 36 or count < 0:

            await ctx.send("Нужно выбрать число от 0 до 36")

        elif amount > balance or amount < 0:

            await ctx.send("Недостаточно :leaves:, иди на работу.")

        elif balance <= 0:

            await ctx.send("Недостаточно :leaves:, иди на работу.")

        else:

            if count != number:
                dogactive = cursor.execute("SELECT dogactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
                    0]
                if dogactive == 1:
                    if amount <= 100:
                        cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
                        connection.commit()
                        embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                        embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
                        embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
                        await ctx.send(embed=embed)

                    else:
                        dogeffect = 5 * (1/100) * amount
                        roundup = math.ceil(dogeffect)
                        cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
                        cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(roundup, ctx.author.id))
                        connection.commit()
                        embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                        embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
                        embed.add_field(name='За счет того что у вас есть питомец "Собака", вам вернули:', value=f'{roundup} SH', inline=False)
                        embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
                        await ctx.send(embed=embed)
                
                else:
                    cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
                    connection.commit()
                    embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                    embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
                    embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
                    await ctx.send(embed=embed)

            elif count == number:
                wolfactive = cursor.execute("SELECT wolfactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
                    0]
                # Если есть волк
                if wolfactive == 1:
                    win = amount * 36
                    wolfeffect = 7 * (1 / 100) * win
                    roundup = math.ceil(wolfeffect)
                    result = win + roundup
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(result, ctx.author.id))
                    connection.commit()
                    embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                    embed.add_field(name='Поздравляю! Вы выйграли:',
                                    value=f'{amount * 36} SH + Бонус: {roundup} SH за счет того что у вас есть питомец "Волк".',
                                    inline=False)
                    embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
                    await ctx.send(embed=embed)
                else:
                    cursor.execute(
                        "UPDATE users SET money = money + {} WHERE id = {}".format(amount * 36, ctx.author.id))
                    connection.commit()
                    embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                    embed.add_field(name='Поздравляю! Вы выйграли:', value=f'{amount * 36} SH.', inline=False)
                    embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
                    await ctx.send(embed=embed)

    @commands.command(aliases=["кейс", "кейсы", "контейнер"])
    async def case(self, ctx, move: str = None):

        moves = ["открыть", "купить", "buy", "open"]
        keys = cursor.execute("SELECT keys FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        connection = data_base

        if move is None:

            embed = discord.Embed(title=f'[CASE]', color=0x42f566)
            embed.add_field(name='У вас в наличии:', value=f'{keys} кейсов.', inline=False)
            await ctx.send(embed=embed)

        elif move is not None and move not in moves:

            emb = discord.Embed(title='[ERROR] сase', description=f'{ctx.author.mention}, Укажите правильное действие!',
                                colour=discord.Colour(0xe73c3c))
            emb.add_field(name='Действия:', value=f'{moves}', inline=False)
            emb.add_field(name='Пример :', value='/case открыть')
            await ctx.send(embed=emb)

        elif move in ['окрыть', 'open']:

            keys = cursor.execute("SELECT keys FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            connection = data_base
            val = 1

            if keys >= 1:

                cursor.execute("UPDATE users SET keys = keys - {} WHERE id = {}".format(val, ctx.author.id))
                connection.commit()
                rand = random.randint(0, 100)

                if 0 <= rand <= 70:
                    pp0 = 1000
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp0, ctx.author.id))
                    connection.commit()
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успено открыли кейс.', value="Вам выпало 1.000SH", inline=False)
                    await ctx.send(embed=emb)

                elif 71 <= rand <= 80:

                    pp1 = 15000
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp1, ctx.author.id))
                    connection.commit()
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успено открыли кейс.', value="Вам выпало 15.000SH", inline=False)
                    await ctx.send(embed=emb)

                elif 81 <= rand <= 90:

                    pp2 = 22500
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp2, ctx.author.id))
                    connection.commit()
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успено открыли кейс.', value="Вам выпало 22.500SH", inline=False)
                    await ctx.send(embed=emb)

                elif 91 <= rand <= 95:

                    pp3 = 50000
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp3, ctx.author.id))
                    connection.commit()
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успешно открыли кейс.', value="Вам выпало 50.000SH", inline=False)
                    await ctx.send(embed=emb)

                elif 96 <= rand <= 100:

                    pp3 = 100000
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp3, ctx.author.id))
                    connection.commit()
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успешно открыли кейс.', value="Вам выпало 100.000SH", inline=False)
                    await ctx.send(embed=emb)

            elif keys < 1:

                emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Ошибка.', value="У вас нет кейсов.", inline=False)
                await ctx.send(embed=emb)

        elif move in ['buy', 'купить']:

            cent = 10000  # Цена кейса
            val = 1  # Кол-во покупаемых кейсов.
            if balance < cent:

                emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Ошибка.', value="Недостаточно средств.", inline=False)
                await ctx.send(embed=emb)

            elif balance >= cent:

                cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(cent, ctx.author.id))
                cursor.execute("UPDATE users SET keys = keys + {} WHERE id = {}".format(val, ctx.author.id))
                connection.commit()
                emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Успешно.',
                              value="Кейс был куплен, для открытия введите '/case открыть или /case open'.",
                              inline=False)
                await ctx.send(embed=emb)

    ##############  ЗАДУМКА ##############
    # Из кейсов с питомцами , с очень маленьким шансом могут упасть питомцы , которые будут давать какие либо положительные эффекты.
    # Пример N1. После победы в казино , если есть определенный питомец будет сверху прибавлятся пару процентов от выйгрыша.
    # Пример N2. После выхода из войса будут бонусные SH за время проведенное в войсе.
    # Это пока что пару примеров которые попробую реализовать , далее с приходом идеи о новом питомце можно будет добавлять новых.

    # casepets открыть не работает, хз почему
    @commands.command(aliases=["питомцы", "кейс с питомцами", "питомец кейс"])  # Кейсы с питомцами
    async def casepets(self, ctx, move: str = None):

        moves = ["открыть", "купить", "buy", "open"]
        wolfpets = cursor.execute("SELECT wolfpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        foxpets = cursor.execute("SELECT foxpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        dogpets = cursor.execute("SELECT dogpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        casepets = cursor.execute("SELECT casepets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        connection = data_base

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

            casepets = cursor.execute("SELECT casepets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            connection = data_base
            val = 1

            if casepets >= 1:
                cursor.execute("UPDATE users SET casepets = casepets - {} WHERE id = {}".format(val, ctx.author.id))
                connection.commit()
                rand = random.randint(0, 50)

                if rand == 31:

                    if wolfpets == 1:
                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='[Итог]', value="Вам бы выпал питомец 'Волк', но он у вас уже есть.",
                                      inline=False)
                        await ctx.send(embed=emb)

                    else:
                        cursor.execute(
                            "UPDATE users SET wolfpets = wolfpets + {} WHERE id = {}".format(val, ctx.author.id))
                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='Поздравляем.', value="Вам выпал питомец 'Волк'.", inline=False)
                        emb.add_field(name='Питомец "Волк".',
                                      value="Данный питомец прибавляет процент от суммы выйгрыша в казино на 7% .",
                                      inline=False)
                        emb.add_field(name='Пример:".',
                                      value="Вы сыграли в казино на 50.000 SH, победили, вам прибавляется на баланс 50.000 SH которые вы выйграли и сверху 3.500 SH за счет того что у вас данный питомец .",
                                      inline=False)
                        emb.add_field(name='Посмотреть ваших питомцев:', value="/mypets", inline=False)
                        emb.add_field(name='Узнать информацию о всех питомцах', value="/help питомцы", inline=False)
                        await ctx.send(embed=emb)

                elif rand == 14:
                    if foxpets == 1:
                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='[Итог]', value="Вам бы выпал питомец 'Лиса', но он у вас уже есть.",
                                      inline=False)
                        await ctx.send(embed=emb)

                    else:
                        cursor.execute(
                            "UPDATE users SET foxpets = foxpets + {} WHERE id = {}".format(val, ctx.author.id))
                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='Поздравляем.', value="Вам выпал питомец 'Лиса'.", inline=False)
                        emb.add_field(name='Питомец "Лиса".',
                                      value="Данный питомец прибавляет 7% SH от времени которое вы находились в голосовом канале.",
                                      inline=False)
                        emb.add_field(name='Пример:".',
                                      value="Вы просидели в голосовом канале 4 часа, после выхода вас начислятся 4.800 SH, за счет того что у вас данный питомец , вам сверху прибавится 336 SH.",
                                      inline=False)
                        emb.add_field(name='Посмотреть ваших питомцев:', value="/mypets", inline=False)
                        emb.add_field(name='Узнать информацию о всех питомцах', value="/help питомцы", inline=False)
                        await ctx.send(embed=emb)

                elif rand == 37:
                    if dogpets == 1:
                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='[Итог]', value="Вам бы выпал питомец 'Собака', но он у вас уже есть.",
                                      inline=False)
                        await ctx.send(embed=emb)

                    else:
                        cursor.execute(
                            "UPDATE users SET dogpets = dogpets + {} WHERE id = {}".format(val, ctx.author.id))
                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='Поздравляем.', value="Вам выпал питомец 'Собака'.", inline=False)
                        emb.add_field(name='Питомец "Собака".',
                                      value="Данный питомец возвращает вам 5 % от проигрыша в казино.",
                                      inline=False)
                        emb.add_field(name='Пример:".',
                                      value="Вы поставили в казино 5000 SH и проиграли , за счет того что у вас данный питомец, вам вернется 250 SH. :exclamation: Если ставка менее 100 SH возврата средств не будет :exclamation: ",
                                      inline=False)
                        emb.add_field(name='Посмотреть ваших питомцев:', value="/mypets", inline=False)
                        emb.add_field(name='Узнать информацию о всех питомцах', value="/help питомцы", inline=False)
                        await ctx.send(embed=emb)




                else:
                    emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='[Итог]', value="К сожалению вам ничего не выпало.",
                                  inline=False)
                    await ctx.send(embed=emb)

            elif casepets <= 0:

                emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Ошибка.', value="У вас нет кейсов.", inline=False)
                await ctx.send(embed=emb)
=======

# class Gambling(commands.Cog):
#
#     def __init__(self):
#         self.bot = bot
#
#     @commands.command(aliases=['Казино', 'казино', 'casino', 'Casino'])
#     async def __casino(self, ctx, amount: int = None):
#         balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
#         connection = data_base
#         number = random.randint(1, 100)
#         jackpot = amount * 5
#
#         # Условия и т.д
#
#         if amount is None:
#
#             emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
#             emb.add_field(name='[Ошибка]', value="Вы забыли указать ставку!", inline=False)
#             await ctx.send(embed=emb)
#
#         elif amount > balance or amount < 0:
#
#             emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
#             emb.add_field(name='[Ошибка]', value="Недостаточно средств.", inline=False)
#             await ctx.send(embed=emb)
#
#         elif balance <= 0:
#
#             emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
#             emb.add_field(name='[Ошибка]', value="Недостаточно средств.", inline=False)
#             await ctx.send(embed=emb)
#
#         else:
#
#             if number < 50:
#                 dogavtive = \
#                     cursor.execute("SELECT dogactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
#                         0]
#                 if dogavtive == 1:
#                     if amount <= 100:
#                         cursor.execute(
#                             "UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
#                         connection.commit()
#                         embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                         embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
#                         await ctx.send(embed=embed)
#                     else:
#                         dogeffect = 5 * (1 / 100) * amount
#                         roundup = math.ceil(dogeffect)
#                         cursor.execute(
#                             "UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
#                         cursor.execute(
#                             "UPDATE users SET money = money + {} WHERE id = {}".format(roundup, ctx.author.id))
#                         connection.commit()
#                         embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                         embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
#                         embed.add_field(name='За счет того что у вас есть питомец собака, вам вернули',
#                                         value=f'{roundup} SH', inline=False)
#                         await ctx.send(embed=embed)
#                 else:
#                     cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
#                     connection.commit()
#                     embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                     embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
#                     await ctx.send(embed=embed)
#
#             elif number == 93:
#                 wolfactive = \
#                     cursor.execute("SELECT wlofactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
#                         0]
#                 if wolfactive == 1:
#                     wolfeffect = 7 * (1 / 100) * jackpot
#                     roundup = math.ceil(wolfeffect)  # Округление
#                     result = jackpot + roundup
#                     cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(result, ctx.author.id))
#                     embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                     embed.add_field(name='О боже мой!!! Вы выйграли JACKPOT, мы добавили вам на баланс:',
#                                     value=f'{jackpot} SH + Бонус: {roundup} SH за счет того что у вас есть питомец '
#                                           f'"Волк".',
#                                     inline=False)
#                     await ctx.send(embed=embed)
#
#                 else:
#                     embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                     embed.add_field(name='О боже мой!!! Вы выйграли JACKPOT, мы добавили вам на баланс:',
#                                     value=f'{jackpot} SH', inline=False)
#                     await ctx.send(embed=embed)
#
#             elif number == 27:
#
#                 emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
#                 emb.add_field(name='[Итог]', value="Вам попалось SAFE-ЯЧЕЙКА, вы не потеряли свой баланс.",
#                               inline=False)
#                 await ctx.send(embed=emb)
#
#             elif number == 13:
#
#                 emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
#                 emb.add_field(name='[Итог]', value="Вам попалось SAFE-ЯЧЕЙКА, вы не потеряли свой баланс.",
#                               inline=False)
#                 await ctx.send(embed=emb)
#
#             else:
#                 wolfactive = \
#                     cursor.execute("SELECT wolfactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
#                         0]
#                 if wolfactive == 1:
#
#                     wolfeffect = 7 * (1 / 100) * amount
#                     roundup = math.ceil(wolfeffect)
#                     result = amount + roundup
#                     cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(result, ctx.author.id))
#                     connection.commit()
#                     embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                     embed.add_field(name='Поздравляю! Вы выйграли:',
#                                     value=f'{amount} SH + Бонус: {roundup} SH за счет того что у вас есть питомец '
#                                           f'"Волк".',
#                                     inline=False)
#                     await ctx.send(embed=embed)
#
#                 else:
#                     cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(amount, ctx.author.id))
#                     connection.commit()
#                     embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                     embed.add_field(name='Поздравляю! Вы выйграли:', value=f'{amount} SH', inline=False)
#                     await ctx.send(embed=embed)
#
#     @commands.command()
#     async def roulette(self, ctx, amount: int = None, count: int = None):
#         connection = data_base
#         number = random.randint(0, 36)
#         balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
#
#         if amount is None:
#
#             await ctx.send("Вы забыли указать ставку!")
#
#         elif count is None:
#
#             await ctx.send("Нужно выбрать на что ставить.")
#
#         elif count > 36 or count < 0:
#
#             await ctx.send("Нужно выбрать число от 0 до 36")
#
#         elif amount > balance or amount < 0:
#
#             await ctx.send("Недостаточно :leaves:, иди на работу.")
#
#         elif balance <= 0:
#
#             await ctx.send("Недостаточно :leaves:, иди на работу.")
#
#         else:
#
#             if count != number:
#                 dogactive = \
#                     cursor.execute("SELECT dogactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
#                         0]
#                 if dogactive == 1:
#                     if amount <= 100:
#                         cursor.execute(
#                             "UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
#                         connection.commit()
#                         embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                         embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
#                         embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
#                         await ctx.send(embed=embed)
#
#                     else:
#                         dogeffect = 5 * (1 / 100) * amount
#                         roundup = math.ceil(dogeffect)
#                         cursor.execute(
#                             "UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
#                         cursor.execute(
#                             "UPDATE users SET money = money + {} WHERE id = {}".format(roundup, ctx.author.id))
#                         connection.commit()
#                         embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                         embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
#                         embed.add_field(name='За счет того что у вас есть питомец "Собака", вам вернули:',
#                                         value=f'{roundup} SH', inline=False)
#                         embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
#                         await ctx.send(embed=embed)
#
#                 else:
#                     cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
#                     connection.commit()
#                     embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                     embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
#                     embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
#                     await ctx.send(embed=embed)
#
#             elif count == number:
#                 wolfactive = \
#                     cursor.execute("SELECT wolfactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[
#                         0]
#                 # Если есть волк
#                 if wolfactive == 1:
#                     win = amount * 36
#                     wolfeffect = 7 * (1 / 100) * win
#                     roundup = math.ceil(wolfeffect)
#                     result = win + roundup
#                     cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(result, ctx.author.id))
#                     connection.commit()
#                     embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                     embed.add_field(name='Поздравляю! Вы выйграли:',
#                                     value=f'{amount * 36} SH + Бонус: {roundup} SH за счет того что у вас есть '
#                                           f'питомец "Волк".',
#                                     inline=False)
#                     embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
#                     await ctx.send(embed=embed)
#                 else:
#                     cursor.execute(
#                         "UPDATE users SET money = money + {} WHERE id = {}".format(amount * 36, ctx.author.id))
#                     connection.commit()
#                     embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
#                     embed.add_field(name='Поздравляю! Вы выйграли:', value=f'{amount * 36} SH.', inline=False)
#                     embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
#                     await ctx.send(embed=embed)
#
#     @commands.command(aliases=["кейс", "кейсы", "контейнер"])
#     async def case(self, ctx, move: str = None):
#
#         moves = ["открыть", "купить", "buy", "open"]
#         keys = cursor.execute("SELECT keys FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
#         balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
#         connection = data_base
#
#         if move is None:
#
#             embed = discord.Embed(title=f'[CASE]', color=0x42f566)
#             embed.add_field(name='У вас в наличии:', value=f'{keys} кейсов.', inline=False)
#             await ctx.send(embed=embed)
#
#         elif move is not None and move not in moves:
#
#             emb = discord.Embed(title='[ERROR] сase', description=f'{ctx.author.mention}, Укажите правильное действие!',
#                                 colour=discord.Colour(0xe73c3c))
#             emb.add_field(name='Действия:', value=f'{moves}', inline=False)
#             emb.add_field(name='Пример :', value='/case открыть')
#             await ctx.send(embed=emb)
#
#         elif move in ['окрыть', 'open']:
#
#             keys = cursor.execute("SELECT keys FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
#             connection = data_base
#             val = 1
#
#             if keys >= 1:
#
#                 cursor.execute("UPDATE users SET keys = keys - {} WHERE id = {}".format(val, ctx.author.id))
#                 connection.commit()
#                 rand = random.randint(0, 100)
#
#                 if 0 <= rand <= 70:
#                     pp0 = 1000
#                     cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp0, ctx.author.id))
#                     connection.commit()
#                     emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
#                     emb.add_field(name='Вы успено открыли кейс.', value="Вам выпало 1.000SH", inline=False)
#                     await ctx.send(embed=emb)
#
#                 elif 71 <= rand <= 80:
#
#                     pp1 = 15000
#                     cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp1, ctx.author.id))
#                     connection.commit()
#                     emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
#                     emb.add_field(name='Вы успено открыли кейс.', value="Вам выпало 15.000SH", inline=False)
#                     await ctx.send(embed=emb)
#
#                 elif 81 <= rand <= 90:
#
#                     pp2 = 22500
#                     cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp2, ctx.author.id))
#                     connection.commit()
#                     emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
#                     emb.add_field(name='Вы успено открыли кейс.', value="Вам выпало 22.500SH", inline=False)
#                     await ctx.send(embed=emb)
#
#                 elif 91 <= rand <= 95:
#
#                     pp3 = 50000
#                     cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp3, ctx.author.id))
#                     connection.commit()
#                     emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
#                     emb.add_field(name='Вы успешно открыли кейс.', value="Вам выпало 50.000SH", inline=False)
#                     await ctx.send(embed=emb)
#
#                 elif 96 <= rand <= 100:
#
#                     pp3 = 100000
#                     cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp3, ctx.author.id))
#                     connection.commit()
#                     emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
#                     emb.add_field(name='Вы успешно открыли кейс.', value="Вам выпало 100.000SH", inline=False)
#                     await ctx.send(embed=emb)
#
#             elif keys < 1:
#
#                 emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
#                 emb.add_field(name='Ошибка.', value="У вас нет кейсов.", inline=False)
#                 await ctx.send(embed=emb)
#
#         elif move in ['buy', 'купить']:
#
#             cent = 10000  # Цена кейса
#             val = 1  # Кол-во покупаемых кейсов.
#             if balance < cent:
#
#                 emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
#                 emb.add_field(name='Ошибка.', value="Недостаточно средств.", inline=False)
#                 await ctx.send(embed=emb)
#
#             elif balance >= cent:
#
#                 cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(cent, ctx.author.id))
#                 cursor.execute("UPDATE users SET keys = keys + {} WHERE id = {}".format(val, ctx.author.id))
#                 connection.commit()
#                 emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
#                 emb.add_field(name='Успешно.',
#                               value="Кейс был куплен, для открытия введите '/case открыть или /case open'.",
#                               inline=False)
#                 await ctx.send(embed=emb)
#
>>>>>>> Stashed changes

        elif move in ['buy', 'купить']:

            price = 5000  # Цена кейса
            val = 1  # Кол-во покупаемых кейсов.
            if balance < price:

                emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Ошибка.', value="Недостаточно средств.", inline=False)
                await ctx.send(embed=emb)

            elif balance >= price:

                cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(price, ctx.author.id))
                cursor.execute("UPDATE users SET casepets = casepets + {} WHERE id = {}".format(val, ctx.author.id))
                connection.commit()
                emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Успешно.',
                              value="Кейс с питомцами был куплен, для открытия введите '/casepets открыть или /casepets open'.",
                              inline=False)
                await ctx.send(embed=emb)

    @commands.command(aliases=["мои питомцы", "мои петы"])
    async def mypets(self, ctx):
        wolfpets = cursor.execute("SELECT wolfpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        foxpets = cursor.execute("SELECT foxpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        if wolfpets == 1 and foxpets == 0:
            emb = discord.Embed(title="[MyPets]", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Ваши питомцы.', value="У вас есть только питомец 'Волк'.", inline=False)
            emb.add_field(name='Эффект от питомца.',
                          value="Данный питомец прибавляет процент от суммы выйгрыша в казино на 7%.", inline=False)
            await ctx.send(embed=emb)
        elif foxpets == 1 and wolfpets == 0:
            emb = discord.Embed(title="[MyPets]", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Ваши питомцы.', value="У вас есть только питомец 'Лиса'.", inline=False)
            emb.add_field(name='Эффект от питомца.',
                          value="Данный питомец прибавляет 7% SH от времени которое вы находились в голосовом канале.",
                          inline=False)
            await ctx.send(embed=emb)
        elif foxpets == 1 and wolfpets == 1:
            emb = discord.Embed(title="[MyPets]", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Ваши питомцы.', value="У вас есть 2 питомца, 'Волк' и 'Лиса'.", inline=False)
            emb.add_field(name='Эффекты от питомцев.',
                          value="'Волк' - Данный питомец прибавляет процент от суммы выйгрыша в казино на 7%. 'Лиса' - Данный питомец прибавляет 7% SH от времени которое вы находились в голосовом канале.",
                          inline=False)
            await ctx.send(embed=emb)
        elif foxpets == 0 and wolfpets == 0:
            emb = discord.Embed(title="[MyPets]", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Ваши питомцы.', value="У вас нет питомцев :(", inline=False)
            await ctx.send(embed=emb)

    @commands.command()  # Выбрать питомца
    async def selectpet(self, ctx, move: str = None):
        select = Select(

            options=[
            discord.SelectOption(
                label="Wolf", 
                emoji="🐺"
            ),

            discord.SelectOption(
                label="Fox", 
                emoji="🦊"
            ),

            discord.SelectOption(
                label="Dog", 
                emoji="🐶"
            )
        ])

        async def my_callback(interaction): # Если namepet active - выбран данный питомец
            val = 1
            wolfpet = cursor.execute("SELECT wolfpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            foxpet = cursor.execute("SELECT foxpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            dogpet = cursor.execute("SELECT dogpets FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            wolfactive = cursor.execute("SELECT wolfactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            foxactive = cursor.execute("SELECT foxactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            dogactive = cursor.execute("SELECT dogactive FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            connection = data_base
            if select.values[0] == "Wolf":
                if wolfpet == 0:
                    await ctx.send("У вас нет данного питомца.")
                else:
                    if wolfactive == 1:
                        await ctx.send("У вас установлен данный питомец.")
                    elif wolfactive == 0 and foxactive == 0 and dogactive == 0:
                        cursor.execute("UPDATE users SET wolfactive = wolfactive + {} WHERE id = {}".format(val, ctx.author.id))
                        connection.commit()
                    elif wolfactive == 0 and foxactive >= 1 and dogactive >= 1:
                        await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
                        cursor.execute("UPDATE users SET wolfactive = wolfactive + {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET foxactive = foxactive - {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET dogactive = dogactive - {} WHERE id = {}".format(val, ctx.author.id))
                        
                        connection.commit()
                    elif wolfactive == 0 and foxactive >= 1 and dogactive == 0:
                        await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
                        cursor.execute("UPDATE users SET wolfactive = wolfactive + {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET foxactive = foxactive - {} WHERE id = {}".format(val, ctx.author.id))
                        
                        connection.commit()
                    elif wolfactive == 0 and foxactive == 0 and dogactive >= 1:
                        await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
                        cursor.execute("UPDATE users SET wolfactive = wolfactive + {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET dogactive = dogactive - {} WHERE id = {}".format(val, ctx.author.id))
                        
                        connection.commit()

            elif select.values[0] == "Fox":
                if foxpet == 0:
                    await ctx.send("У вас нет данного питомца.")
                else:
                    if foxactive == 1:
                        await ctx.send("У вас установлен данный питомец.")
                    elif wolfactive == 0 and foxactive == 0 and dogactive == 0:
                        await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
                        cursor.execute("UPDATE users SET foxactive = foxactive + {} WHERE id = {}".format(val, ctx.author.id))
                        connection.commit()
                    elif wolfactive >= 1 and foxactive == 0 and dogactive >= 1:
                        await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
                        cursor.execute("UPDATE users SET foxactive = foxactive + {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET wolfactive = wolfactive - {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET dogactive = dogactive - {} WHERE id = {}".format(val, ctx.author.id))
                        connection.commit()
                    elif wolfactive >= 0 and foxactive == 0 and dogactive == 0:
                        await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
                        cursor.execute("UPDATE users SET foxactive = foxactive + {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET wolfactive = wolfactive - {} WHERE id = {}".format(val, ctx.author.id))
                        connection.commit()
                    elif wolfactive >= 0 and foxactive == 0 and dogactive >= 1:
                        await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
                        cursor.execute("UPDATE users SET foxactive = foxactive + {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET dogactive = dogactive - {} WHERE id = {}".format(val, ctx.author.id))
                        
                        connection.commit()

            elif select.values[0] == "Dog":
                if dogpet == 0:
                    await ctx.send("У вас нет данного питомца.")
                else:
                    if dogactive == 1:
                        await ctx.send("У вас установлен данный питомец.")
                    elif wolfactive == 0 and foxactive == 0 and dogactive == 0:
                        await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
                        cursor.execute("UPDATE users SET dogactive = dogactive + {} WHERE id = {}".format(val, ctx.author.id))
                        connection.commit()
                    elif wolfactive == 1 and foxactive == 1 and dogactive == 0:
                        await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
                        cursor.execute("UPDATE users SET wolfactive = wolfactive - {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET foxactive = foxactive - {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET dogactive = dogactive + {} WHERE id = {}".format(val, ctx.author.id))
                        connection.commit()
                    elif dogactive == 0 and wolfactive >= 1 and foxactive == 0:
                        await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
                        cursor.execute("UPDATE users SET wolfactive = wolfactive - {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET dogactive = dogactive + {} WHERE id = {}".format(val, ctx.author.id))
                        connection.commit()
                    elif dogactive == 0 and wolfactive == 0 and foxactive >= 1:
                        await interaction.response.send_message(f"Выбран питомец: {select.values[0]}")
                        cursor.execute("UPDATE users SET foxactive = foxactive - {} WHERE id = {}".format(val, ctx.author.id))
                        cursor.execute("UPDATE users SET dogactive = dogactive + {} WHERE id = {}".format(val, ctx.author.id))
                        connection.commit()

        select.callback = my_callback
        view = View()
        view.add_item(select)
        await ctx.send("Select Pet",view=view)


async def setup(bot):
    await bot.add_cog(Gambling())
