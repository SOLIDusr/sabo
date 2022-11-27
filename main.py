import discord
import sqlite3
from discord.ext import commands
from config import *
import time
import math
import random

# Создание intents для работы с намерениями
intents = discord.Intents.all()
q = 0
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

data_base = sqlite3.connect('bot_test.db', timeout=10)
cursor = data_base.cursor()


@bot.event
async def on_ready():
    print('Bot launched successfully :)')
    print(f'My name is {bot.user.name}')
    print(f'My client id is {bot.user.id}')
    for guild in bot.guilds:
        print(f'Connected to server, id is: {guild.id}')
        for member in guild.members:
            cursor.execute(f"SELECT id FROM users where id={member.id}")
            if cursor.fetchone() is None:
                cursor.execute(
                    f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', 0)")
            else:
                pass
            data_base.commit()


@bot.event
async def on_ready():
    print('Bot Connected')
    global tdict
    tdict = {}
    await bot.change_presence(activity = discord.Game('r!help'))

@bot.event # Узнает время в войсе
async def on_voice_state_update(member, before, after):
    author = member.id
    if before.channel is None and after.channel is not None:
        t1 = time.time()
        tdict[author] = t1
    elif before.channel is not None and after.channel is None and author in tdict:
        t2 = time.time() 
        t3 = t2-tdict[author]
        global qwe
        q = math.ceil(t3)# Округление времени в войсе
        print(q) #10 за минуту
        qe = q / 60 #Первод секунд в минуту
        qwe = math.ceil(qe) #Округление 
        

@bot.command()
async def work(ctx):
    
    if qwe <= 1: # Проверка на время в войсе (Менее одной минуты или нет)
        await ctx.send("Недостаточно проведено времени в голосовом канале.") # Надо доделать ( не выводит )
    elif qwe > 1:
        qwer = qwe * 5 # Начисление за проведенный промежуток времени
        for row in cursor.execute(f'SELECT money FROM users where id={ctx.author.id}'):
            cursor.execute(f'UPDATE users SET money={(qwer) + row[0]} where id={ctx.author.id}')
            embed = discord.Embed(title=f'Пополнение баланса...', color=0x42f566)
            embed.add_field(name='Баланс был пополнен на:', value=f'{qwer} SH', inline=False)
            await ctx.send(embed=embed)
        data_base.commit()


@bot.command(aliases = ['Казино', 'казино', 'casino', 'Casino']) # Казино 

async def __casino(ctx, amount: int = None):
    connection = sqlite3.connect('bot_test.db')# Подключение к бд
    cursor = connection.cursor()
    number = random.randint(1, 100)

    jackpot = random.randint(5000, 20000)

    
    balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]# Присваиваем баланс из бд к переменной
    # Условия и т.д
    if amount is None:
        await ctx.send("Вы забыли указать ставку!")
    elif amount > balance or amount < 0:
        await ctx.send("Недостаточно :leaves:, иди на работу.")
    elif balance <= 0:
        await ctx.send("Недостаточно :leaves:, иди на работу.")
    
    else:
        if number < 50:
            cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
            connection.commit()
            embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
            embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
            await ctx.send(embed=embed)
           

        elif number == 93:
            cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(jackpot, ctx.author.id))
            connection.commit()
            embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
            embed.add_field(name='О боже мой!!! Вы выйграли JACKPOT, мы добавили вам на баланс:', value=f'{jackpot} SH', inline=False)
            await ctx.send(embed=embed)
            

        elif number == 27:
            await ctx.send('🤡[CASINO]🤡, Вам попалось SAFE-ЯЧЕЙКА, вы не потеряли свой баланс')

        elif number == 13:
            await ctx.send('🤡[CASINO]🤡, Вам попалось SAFE-ЯЧЕЙКА, вы не потеряли свой баланс')

        else:
            cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(amount, ctx.author.id))
            connection.commit()

            embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
            embed.add_field(name='Поздравляю! Вы выйграли:', value=f'{amount} SH', inline=False)
            await ctx.send(embed=embed)

            


@bot.command()
async def roulette(ctx, amount: int = None, count: int = None):
    connection = sqlite3.connect('bot_test.db')
    cursor = connection.cursor()
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
            cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
            connection.commit()
            embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
            embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
            embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
            await ctx.send(embed=embed)
            
        elif count == number:
            cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(amount * 36, ctx.author.id))
            connection.commit()
            embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
            embed.add_field(name='Поздравляю! Вы выйграли:', value=f'{amount*36} SH', inline=False)
            embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
            await ctx.send(embed=embed)
            


@bot.command()
async def balance(ctx):
    for row in cursor.execute(f"SELECT nickname, money FROM users where id={ctx.author.id}"):
        embed = discord.Embed(title=f'Аккаунт пользователя {row[0]}', color=0x42f566)
        embed.add_field(name='Баланс:', value=f'{row[1]} SH', inline=False)
        await ctx.send(embed=embed)


async def give_money(ctx, mention, money):
    try: 
        mention = str(mention).replace('!', '')
        for row in cursor.execute(f'SELECT money FROM users where mention=?', (mention,)):
            cursor.execute(f'UPDATE users SET money={int(money) + row[0]} where mention=?', (mention,))
        data_base.commit()
        for row in cursor.execute(f'SELECT nickname FROM users where mention=?', (mention,)):
            embed = discord.Embed(title='Пополнение баланса', color=0x42f566)
            embed.set_author(name='Community Bot')
            embed.add_field(name='Оповещение', value=f'Баланс пользователя {row[0]} пополнен на {money} SH')
            await ctx.send(embed=embed)
    except Exception as E:
        print(f'give_money command error: {E}')
        embed = discord.Embed(title='Оповещение', color=0xFF0000)
        embed.add_field(name='Оповещение', value='Ошибка при выполнение программы.')
        await ctx.send(embed=embed)


bot.run(settings['token'])
