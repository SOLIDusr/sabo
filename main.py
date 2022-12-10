import discord
import sqlite3
from discord.ext import commands
from config import *
import time
import math
import random

#global variables
global payment1
global channelid
global Oplata # Переменная в которой будет хранится оплаченная за команту сумма
global vtime


intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

data_base = sqlite3.connect('bot_test.db', timeout=10)
cursor = data_base.cursor()




#bot.event
@bot.event
async def on_ready():
    print('Bot launched successfully :)')
    print(f'My name is {bot.user.name}')
    print(f'My client id is {bot.user.id}')
    print('Bot Connected')
    global tdict
    tdict = {}
    await bot.add_cog(Info())
    await bot.add_cog(Gambling())
    await bot.add_cog(CommandsMoney())
    await bot.add_cog(CommandsRoles())
    await bot.change_presence(activity = discord.Game('/Shelp'))
    for guild in bot.guilds:
        print(f'Connected to server, id is: {guild.id}')

@bot.event 
async def on_voice_state_update(member, before, after): #Удаляет войс 
    
    payment2 = int(payment1)
    if payment2 < 12000: # Если денег на Payment нет , - войс
        cchanelid = channelid
        channel = bot.get_channel(cchanelid)
        await channel.delete()
    else:
        pass

@bot.event # Узнает время в войсе
async def on_voice_state_update(member, before, after):
    author = member.id
    if before.channel is None and after.channel is not None:
        t1 = time.time()
        tdict[author] = t1
    elif before.channel is not None and after.channel is None and author in tdict:
        t2 = time.time() 
        t3 = t2-tdict[author]
        tround = math.ceil(t3)
        vtim = tround / 60
        vtime = math.ceil(vtim)
        if vtime <= 1: # Проверка на время в войсе (Менее одной минуты или нет)
            pass 
        elif vtime > 1:
            vtimer = vtime * 10 # Начисление за проведенный промежуток времени
            for row in cursor.execute(f'SELECT money FROM users where id={member.id}'):
                cursor.execute(f'UPDATE users SET money={(vtimer) + row[0]} where id={member.id}')
            data_base.commit()


#commands
class Info(commands.Cog):
    def __init__(self):
        self.bot = bot

    @commands.command()
    async def Shelp(self, ctx):

        he1 = discord.Embed(title="Основные команды", colour=discord.Colour(0x3e038c))
        he1.add_field(name='/casinohelp', value="Узнать о том какие игры есть на сервере и как они работают.:leaves:", inline=False)
        he1.add_field(name='/Valhelp', value="Узнать о том что за валюта есть на данном сервере и все о ней.:leaves:", inline=False)
        he1.add_field(name='/rolehelp', value="Узнать о покупке кастомной роли.:leaves:", inline=False)
        he1.add_field(name='/voicehelp', value="Узнать о покупке личного голосового канала.:leaves:", inline=False)
        he1.add_field(name='/casehelp', value="Узнать о покупке кейсов.:leaves:", inline=False)
        await ctx.send(embed=he1)


    @commands.command()
    async def Valhelp(self, ctx):

        he1 = discord.Embed(title="ValHelp", colour=discord.Colour(0x3e038c))
        he1.add_field(name='Валюта данного сервера - "SH".', value="Чтобы ее получить нужно находиться в войсе.:leaves:", inline=False)
        he1.add_field(name='Система начисления.', value="1 минута в войсе = 20 SH.:leaves:", inline=False)
        he1.add_field(name='Для чего нужна данная валюта?:leaves:', value="В данный момент на нее можно только играть в казино, в будущем планируется добавления нескольких вариантов тратить SH.:leaves:", inline=False)
        he1.add_field(name='Первый вариант.', value="Создание личного голосового чата , поддержание его за SH (Если валюты не будет хватать , войс будет удален).:leaves:", inline=False)
        he1.add_field(name='Второй вариант.', value="Покупка различных ролей а так же создание кастомной роли.:leaves:", inline=False)
        await ctx.send(embed=he1)

    @commands.command()
    async def casinohelp(self, ctx):

        he1 = discord.Embed(title="CasinoHelp", colour=discord.Colour(0x3e038c))
        he1.add_field(name='Игры Casino:', value="--->", inline=False)
        he1.add_field(name='Первая игра.', value='/casino ставка.''В данной игре при победе вы получаете x2 от ставки, в случае проигрыша отнимается сумма вашей ставки. Так же есть шанс словить "JACKPOT", а приз там весьма неплохой.:leaves:', inline=False)
        he1.add_field(name='Вторая игра.', value="/roulette ставка число.""В данной игре рандомно выпадает число от 0 до 36, вы пытаетесь угадать что выпадет и в случае победы вы получаете x36 от суммы ставки.:leaves:", inline=False)
        he1.add_field(name='Откуда брать валюту для игры в Казино?:leaves:', value="/Valhelp", inline=False)
        await ctx.send(embed=he1)


    @commands.command()
    async def rolehelp(self, ctx):

        he1 = discord.Embed(title="RoleHelp", colour=discord.Colour(0x3e038c))
        he1.add_field(name='Кастомные роли.', value="На нашем сервере есть возможность создать свою роль.", inline=False)
        he1.add_field(name='Цена.', value='Начнем с ценника, стоимость данной услуги составляет 10.000 SH, дорого , но сделано это чтобы у каждого второго не было своей роли, это предаст обладателям кастомной роли некий эксклюзив.', inline=False)
        he1.add_field(name='Создание роли.', value="Создание роли выполняется командой '/newrole Название роли'", inline=False)
        he1.add_field(name='Создал роль. Что дальше?', value="Роль создается 'Дефолтной', так что после покупки вы можете обратиться к @St1zy3 для редакции вашей роли (Цвет, значимость)", inline=False)
        he1.add_field(name='Значимость роли', value='Под значимостью мы подразумеваем то, что роль будет находиться выше остальных и тем самым будет выделять вас.', inline=False)
        await ctx.send(embed=he1)

    @commands.command()
    async def voicehelp(self, ctx):

        he1 = discord.Embed(title="VoiceHelp", colour=discord.Colour(0x3e038c))
        he1.add_field(name='Личная комната.', value="На нашем сервере есть возможность создать свою личную комнату.", inline=False)
        he1.add_field(name='Как создать свою личную комнату?', value='Создание происходит командой "/create_voice", стоимость создания составляет 2.500 SH.', inline=False)
        he1.add_field(name='Оплата личной комнаты.', value="Личную комнату нужно оплачивать, иначе она будет удалена.", inline=False)
        he1.add_field(name='Создал комнату. Что дальше?', value="После создания личной комнаты у вас будет 24 часа на оплату. Оплата недельная , стоимость 7 дней составяет 12.000 SH.", inline=False)
        he1.add_field(name='Как оплатить свою комнату?', value='Оплатить комнату можно командой "/payment".', inline=False)
        he1.add_field(name='Команды управления комнатой.', value='В данный момент есть 2 команды : "/open" - открыть комнату(зайти может каждый), "/lock" - закрыть комнату (никто не может попасть в вашу комнату).', inline=False)
        he1.add_field(name='Могу ли я зарабатывать SH пока нахожусь в своей комнате?', value='Да, можете.', inline=False)
        await ctx.send(embed=he1)

    @commands.command()
    async def casehelp(self,ctx):
        he1 = discord.Embed(title="CaseHelp", colour=discord.Colour(0x3e038c))
        he1.add_field(name='Кейсы.', value="На нашем сервере есть возможность покупать кейсы.", inline=False)
        he1.add_field(name='Как купить кейс?', value='Покупка кейса происходит командой "/buycase".', inline=False)
        he1.add_field(name='Какая стоимость кейса?', value="Стоимость одного кейса составляет 100.000 SH.", inline=False)
        he1.add_field(name='Как узнать сколько у меня кейсов?', value="Это можно сделать командой '/case'.", inline=False)
        he1.add_field(name='Как открыть кейс?', value='Открыть кейс можно при помощи команды "/opencase".', inline=False)
        await ctx.send(embed=he1)

class Gambling(commands.Cog):
    def __init__(self):
        self.bot = bot

    @commands.command(aliases = ['Казино', 'казино', 'casino', 'Casino'])
    async def __casino(self, ctx, amount: int = None):

        connection = sqlite3.connect('bot_test.db')
        cursor = connection.cursor()
        number = random.randint(1, 100)
        jackpot = random.randint(5000, 20000)
        balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        # Условия и т.д
        if amount is None:
            he1 = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='[Ошибка]', value="Вы забыли указать ставку!", inline=False)
            await ctx.send(embed=he1)
        elif amount > balance or amount < 0:
            he1 = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='[Ошибка]', value="Недостаточно средств.", inline=False)
            await ctx.send(embed=he1)
        elif balance <= 0:
            he1 = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='[Ошибка]', value="Недостаточно средств.", inline=False)
            await ctx.send(embed=he1)
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
                he1 = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='[Итог]', value="Вам попалось SAFE-ЯЧЕЙКА, вы не потеряли свой баланс.", inline=False)
                await ctx.send(embed=he1)
            elif number == 13:
                he1 = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='[Итог]', value="Вам попалось SAFE-ЯЧЕЙКА, вы не потеряли свой баланс.", inline=False)
                await ctx.send(embed=he1)
            else:
                cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(amount, ctx.author.id))
                connection.commit()
                embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                embed.add_field(name='Поздравляю! Вы выйграли:', value=f'{amount} SH', inline=False)
                await ctx.send(embed=embed)

    @commands.command()
    async def roulette(self, ctx, amount: int = None, count: int = None):
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

    @commands.command()
    async def buycase(self,ctx):
        connection = sqlite3.connect('bot_test.db')
        cursor = connection.cursor()
        balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        cent = 100000 #Цена кейса
        val = 1 #Кол-во покупаемых кейсов.
        if balance < cent:
            he1 = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Ошибка.', value="Недостаточно средств.", inline=False)           
            await ctx.send(embed=he1)
        elif balance >= cent:
            cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(cent, ctx.author.id))
            connection.commit()
            keys = cursor.execute("SELECT keys FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
            cursor.execute("UPDATE users SET keys = keys + {} WHERE id = {}".format(val, ctx.author.id))
            connection.commit()
            he1 = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Успешно.', value="Кейс был куплен, для открытия введите '/openkeys'.", inline=False)           
            await ctx.send(embed=he1)

    @commands.command()
    async def case(self,ctx):
        connection = sqlite3.connect('bot_test.db')
        cursor = connection.cursor()
        keys = cursor.execute("SELECT keys FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        embed = discord.Embed(title=f'[CASE]', color=0x42f566)
        embed.add_field(name='У вас в наличии:', value=f'{keys} кейсов.', inline=False)          
        await ctx.send(embed=embed)
        

    @commands.command()
    async def opencase(self,ctx):
        connection = sqlite3.connect('bot_test.db')
        cursor = connection.cursor()
        val = 1
        keys = cursor.execute("SELECT keys FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        if keys >= 1:
            cursor.execute("UPDATE users SET keys = keys - {} WHERE id = {}".format(val, ctx.author.id))
            connection.commit()
            rand = random.randint(0,100)
            if rand >=0 and rand <=70:
                he1 = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Вы успено открыли кейс.', value="К сожалению вам ничего не выпало.", inline=False)           
                await ctx.send(embed=he1)
            if rand >= 71 and rand <= 80:
                pp1 = 400000
                cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp1, ctx.author.id))
                connection.commit()
                he1 = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Вы успено открыли кейс.', value="Вам выпало 400.000SH", inline=False)           
                await ctx.send(embed=he1)
            if rand >= 81 and rand <= 90:
                pp2 = 800000
                cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp2, ctx.author.id))
                connection.commit()
                he1 = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Вы успено открыли кейс.', value="Вам выпало 800.000SH", inline=False)           
                await ctx.send(embed=he1)
            if rand >= 91 and rand <= 95:
                pp3 = 1600000
                cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp3, ctx.author.id))
                connection.commit()
                he1 = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Вы успешно открыли кейс.', value="Вам выпало 1.600.000SH", inline=False)           
                await ctx.send(embed=he1)
            if rand >= 96 and rand <= 100:
                pp3 = 5555555
                cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp3, ctx.author.id))
                connection.commit()
                he1 = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Вы успешно открыли кейс.', value="Вам выпало 5.555.555SH", inline=False)           
                await ctx.send(embed=he1)

        elif keys < 1:
            he1 = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Ошибка.', value="У вас нет кейсов.", inline=False)           
            await ctx.send(embed=he1)


class CommandsMoney(commands.Cog):
    def __init__(self):
        self.bot = bot

    @commands.command()
    async def balance(self,ctx):
        for row in cursor.execute(f"SELECT nickname, money FROM users where id={ctx.author.id}"):
            embed = discord.Embed(title=f'Аккаунт пользователя {row[0]}', color=0x42f566)
            embed.add_field(name='Баланс:', value=f'{row[1]} SH', inline=False)
            await ctx.send(embed=embed)
    
    @commands.command()
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
    
    @commands.command()
    async def profile(self,ctx):
        connection = sqlite3.connect('bot_test.db')
        cursor = connection.cursor()
        profilenick = cursor.execute("SELECT nickname FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        profilebalance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        embed = discord.Embed(title=f'[Profile]', color=0x42f566)
        embed.add_field(name='Nickname:', value=f'{profilenick}', inline=False)
        embed.add_field(name='Balance:', value=f'{profilebalance} SH', inline=False)
        await ctx.send(embed=embed)

class CommandsVoice(commands.Cog):
    def __init__(self):
        self.bot = bot

    @commands.command()
    async def create_voice(self,ctx,channel_name):
        connection = sqlite3.connect('bot_test.db')
        cursor = connection.cursor()
        balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]# Присваиваем баланс из бд к переменной
        purchase = 2500
        number = 0
        if balance < purchase:
            he1 = discord.Embed(title="[Payment]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
            await ctx.send(embed=he1)
        elif balance >= purchase:
            cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(purchase, ctx.author.id))
            connection.commit()
            guild = ctx.guild
            channel = await guild.create_voice_channel(channel_name)
            connected = ctx.author.voice
            channel = discord.utils.get(ctx.guild.channels, name=channel_name)
            channelid = channel.id
            print(channelid)
            he1 = discord.Embed(title="[VoiceManager]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Голосовой канал создан.', value="У вас есть 24 часа для того чтобы оплатить голосовой канал, иначе он будет удален.", inline=False)
            he1.add_field(name='Управление каналом.', value="/voicemenu", inline=False)
            he1.add_field(name='Помощь с личным каналом.', value="/voicehelp", inline=False)
            await ctx.send(embed=he1)
            pay = 12000 # Сумма которая будет отниматься за недельную оплату
            def countdown(num_of_secs = 86400): #таймер, количество секунд (num_of_secs), до которого будет отсчитывать таймер (24 часа). (86400)
                while num_of_secs: #Переменная num_of_secs будет непрерывно уменьшаться в цикле, пока не достигнет 0 (что переводится в False и завершает цикл без каких-либо дополнительных условий).
                    m,s = divmod(num_of_secs, 60) # Функция divmod принимает два числа и возвращает произведение и остаток от двух чисел.
                    min_sec_format = '{:02d}:{:02d}'.format(m, s)
                    time.sleep(1)
                    num_of_secs -= 1
                print('Countdown finished.')
                connection = sqlite3.connect('bot_test.db')
                cursor = connection.cursor()
                payment = cursor.execute("SELECT Payment FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]# Присваиваем переменную 
                payment1 = int(payment) 
                if payment1 >= 12000: # Если в поле Payment есть 12000, войс продляется на 7 дней
                    cursor.execute("UPDATE users SET Payment = Payment - {} WHERE id = {}".format(pay, ctx.author.id))
                
                    def countdown1(num_of_secs = 604800): 
                        while num_of_secs: 
                            m,s = divmod(num_of_secs, 60) 
                            min_sec_format = '{:02d}:{:02d}'.format(m, s)
                            time.sleep(1)
                            num_of_secs -= 1
                        print('Countdown finished.')
                  
                    countdown1()
            countdown()
        
    @commands.command() 
    async def voicemenu(self,ctx):
        he1 = discord.Embed(title="Команды упавления личным голосовым чатом.", colour=discord.Colour(0x3e038c))
        he1.add_field(name='/lock', value="Закрывает доступ к комнате.", inline=False)
        he1.add_field(name='/open', value="Открывает доступ к комнате.", inline=False)
        await ctx.send(embed=he1)
        

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def lock(self,ctx):
        await ctx.channel.purge (limit=1)
        channel = ctx.message.author.voice.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.connect = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def open(self,ctx):
        await ctx.channel.purge (limit=1)
        channel = ctx.message.author.voice.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.connect = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    @commands.command
    async def payment(ctx, Oplata):
        connection = sqlite3.connect('bot_test.db')
        cursor = connection.cursor()
        aoplata = int(Oplata)
        balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        if balance >= aoplata:
            cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(aoplata, ctx.author.id)) 
            cursor.execute("UPDATE users SET Payment = Payment + {} WHERE id = {}".format(aoplata, ctx.author.id))
            connection.commit()
            embed = discord.Embed(
            title="Оплата прошла успешно.",
            )
            await ctx.send(embed=embed) 
        elif balance < aoplata:
            he1 = discord.Embed(title="[Payment]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
            await ctx.send(embed=he1)
            

class CommandsRoles(commands.Cog):
    def __init__(self):
        self.bot = bot

    @commands.command()  # создание роли
    async def newrole(ctx, *,content): 
        connection = sqlite3.connect('bot_test.db')
        cursor = connection.cursor()
        a = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] 
        oplata = 10000
        op = a
        connection.commit()
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
    async def shop(self,ctx):
        he1 = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
        he1.add_field(name='Магазин ролей.', value="Ниже представлены роли для покупки.", inline=False)
        he1.add_field(name='1. [1]', value="35.000 SH", inline=False)
        he1.add_field(name='2. [2]', value="50.000 SH", inline=False)
        he1.add_field(name='Покупка.', value="Для покупки необходимо написать '/buyrole Номер роли'", inline=False)
        await ctx.send(embed=he1)
        
    
    @commands.command() # Не работает выдача ролиы
    async def buyrole(self,ctx,count: int = None):
        member = ctx.message.author
        role = discord.Role.name == '[1]'
        oplata = 35000
        role: discord.Role
        member: discord.Member
        connection = sqlite3.connect('bot_test.db')
        cursor = connection.cursor()
        balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] 
        connection.commit()
        if count == 1:
            if balance >= 35000:   
                roles = 1050283874938261544
                role = int(roles)  
                await member.add_roles(roles)
                cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(oplata, ctx.author.id))
                he1 = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Спасибо за покупку!', value="Роль была выдана.", inline=False)
                await ctx.send(embed=he1)
            else:
                he1 = discord.Embed(title="[Buy]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
                await ctx.send(embed=he1)
            
            
bot.run(settings['token'])