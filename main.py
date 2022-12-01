import discord
import sqlite3
from discord.ext import commands
from config import *
import time
import math
import random


# Создание intents для работы с намерениями
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

data_base = sqlite3.connect('bot_test.db', timeout=10)
cursor = data_base.cursor()

global channelid

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
    await bot.change_presence(activity = discord.Game('r!help'))
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


@bot.event # Узнает время в войсе
async def on_voice_state_update(member, before, after):
    
    author = member.id
    if before.channel is None and after.channel is not None:
        t1 = time.time()
        tdict[author] = t1
    elif before.channel is not None and after.channel is None and author in tdict:
        t2 = time.time() 
        t3 = t2-tdict[author]
        global Oplata # Переменная в которой будет хранится оплаченная за команту сумма
        global vtime
        tround = math.ceil(t3)
        # Округление времени в войсе
        vtim = tround / 5
        # Перевод секунд в минуту
        vtime = math.ceil(vtim)
        # Округление
        
        if vtime <= 1: # Проверка на время в войсе (Менее одной минуты или нет)
            pass # Надо доделать ( не выводит )
        elif vtime > 1:
            vtimer = vtime * 25 # Начисление за проведенный промежуток времени
            for row in cursor.execute(f'SELECT money FROM users where id={member.id}'):
                cursor.execute(f'UPDATE users SET money={(vtimer) + row[0]} where id={member.id}')
            data_base.commit()
       
class Info(commands.Cog):
    def __init__(self):
        self.bot = bot

    @commands.command()
    async def Shelp(self, ctx):
        await ctx.send('Help')
        await ctx.send('1. "/casinohelp" - Узнать о том какие игры есть на сервере и как они работают.:leaves:')
        await ctx.send('2. "/Valhelp" - Узнать о том что за валюта есть на данном сервере и все о ней.:leaves:')
        await ctx.send('3. "/rolehelp" - Узнать о покупке кастомной роли.:leaves:')
        await ctx.send('4. "/voicehelp" - Узнать о покупке личного голосового канала.:leaves:')


    @commands.command()
    async def Valhelp(self, ctx):
        await ctx.send('Валюта данного сервера - "SH". Чтобы ее получить нужно находиться в войсе.:leaves:')
        await ctx.send('1 минута в войсе = 50 SH.:leaves:')
        await ctx.send('Для чего нужна данная валюта?:leaves:')
        await ctx.send('В данный момент на нее можно только играть в казино, в будущем планируется добавления нескольких вариантов тратить SH.:leaves:')
        await ctx.send('1. Создание личного голосового чата , поддержание его за SH (Если валюты не будет хватать , войс будет удален).:leaves:')
        await ctx.send('2. Покупка различных ролей а так же создание кастомной роли.:leaves:')


    @commands.command()
    async def casinohelp(self, ctx):
        await ctx.send('Помощь по Casino.')
        await ctx.send('В данном боте есть 2 вида игры в казино на данный момент.')
        await ctx.send('1. "$casino ставка", в данной игре при победе вы получаете x2 от ставки, в случае проигрыша отнимается сумма вашей ставки. Так же есть шанс словить "JACKPOT", а приз там весьма неплохой.:leaves:')
        await ctx.send('2. "$roulette ставка число". В данной игре рандомно выпадает число от 0 до 36, вы пытаетесь угадать что выпадет и в случае победы вы получаете x36 от суммы ставки.:leaves:')
        await ctx.send('Откуда брать валюту для игры в Казино?:leaves:')
        await ctx.send('"$Valhelp"')


    @commands.command()
    async def rolehelp(self, ctx):
        await ctx.send('Так как на сервере есть возможность создания кастомной роли , нужно знать несколько вещей.')
        await ctx.send('Начнем с ценника, стоимость данной услуги составляет 500.000 SH, дорого , но сделано это чтобы у каждого второго не было своей роли, это предаст обладателям кастомной роли некий эксклюзив.')
        await ctx.send('Создание роли выполняется командой "/newrole Название роли"')
        await ctx.send('Роль создается "Дефолтной", так что после покупки вы можете обратиться к @St1zy3 для редакции вашей роли (Цвет, значимость)')
        await ctx.send('Под значимостью мы подразумеваем то, что роль будет находиться выше остальных и тем самым будет выделять вас.')


    @commands.command()
    async def voicehelp(self, ctx):
        await ctx.send('На нашем сервере есть возможность создавать личный голосовой канал.')
        await ctx.send('Создание происходит командой "/create_voice", стоимость создания составляет 10.000 SH.')
        await ctx.send('Личную комнату нужно оплачивать, иначе она будет удалена.')
        await ctx.send('После создания личной комнаты у вас будет 24 часа на оплату. Оплата недельная , стоимость 7 дней составяет 20.000 SH.')
        await ctx.send('Оплатить комнату можно командой "/payment".')
        await ctx.send('Хочу подчеркнуть , что пока вы (Создатель комнаты) находитесь в своей комнате , SH вы получать не будете(Данный пункт в разработке).')
        

class Gambling(commands.Cog):
    def __init__(self):
        self.bot = bot


    @commands.command(aliases = ['Казино', 'казино', 'casino', 'Casino'])
    async def __casino(self, ctx, amount: int = None):
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
            


@bot.command()
async def balance(ctx):
    for row in cursor.execute(f"SELECT nickname, money FROM users where id={ctx.author.id}"):

        embed = discord.Embed(title=f'Аккаунт пользователя {row[0]}', color=0x42f566)
        embed.add_field(name='Баланс:', value=f'{row[1]} SH', inline=False)
        await ctx.send(embed=embed)

@bot.command()
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

#Экономика
#Создание войса  - 10к
#При создании войс может работать 1 день
#Продление войса , 20к - 7 дней
#Оплата недельная , минимум оплатить можно на 7 дней.



@bot.command()
async def create_voice(ctx,channel_name):
     
    connection = sqlite3.connect('bot_test.db')# Подключение к бд
    cursor = connection.cursor()

    balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]# Присваиваем баланс из бд к переменной
    a = 10000
    number = 0
    

    if balance < a:
        await ctx.send("Недостаточно :leaves:, иди на работу.")
    elif balance >= a:

        cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(a, ctx.author.id))
        connection.commit()

        guild = ctx.guild # Создание войса
        channel = await guild.create_voice_channel(channel_name)
        connected = ctx.author.voice
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        await ctx.send("Голосовой канал создан.")
        
        channelid = channel.id
        print(channelid)# Получает id созданного канала
        
        #number = 1 - Голосовой чат оплачен
        #number = 2 - Не оплачен
        #number = 1
        pay = 20000 # Сумма которая будет отниматься за недельную оплату
        await ctx.send("У вас есть 24 часа для того чтобы оплатить голосовой канал, иначе он будет удален.")
        

        def countdown(num_of_secs = 86400): #таймер, количество секунд (num_of_secs), до которого будет отсчитывать таймер (24 часа). (86400)
            while num_of_secs: #Переменная num_of_secs будет непрерывно уменьшаться в цикле, пока не достигнет 0 (что переводится в False и завершает цикл без каких-либо дополнительных условий).
                m,s = divmod(num_of_secs, 60) # Функция divmod принимает два числа и возвращает произведение и остаток от двух чисел.
                min_sec_format = '{:02d}:{:02d}'.format(m, s)
                
                time.sleep(1)
                num_of_secs -= 1

            print('Countdown finished.')
            global g
            connection = sqlite3.connect('bot_test.db')# Подключение к бд
            cursor = connection.cursor()
            a = cursor.execute("SELECT Payment FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]# Присваиваем переменную 
            g = int(a) 

            if g >= 20000: # Если в поле Payment есть 20000, войс продляется на 7 дней
                cursor.execute("UPDATE users SET Payment = Payment - {} WHERE id = {}".format(pay, ctx.author.id))
                
                def countdown1(num_of_secs = 604800): #таймер, количество секунд (num_of_secs), до которого будет отсчитывать таймер (7 дней).
                    while num_of_secs: #Переменная num_of_secs будет непрерывно уменьшаться в цикле, пока не достигнет 0 (что переводится в False и завершает цикл без каких-либо дополнительных условий).
                        m,s = divmod(num_of_secs, 60) # Функция divmod принимает два числа и возвращает произведение и остаток от двух чисел.
                        min_sec_format = '{:02d}:{:02d}'.format(m, s)
                        
                        time.sleep(1)
                        num_of_secs -= 1
                    print('Countdown finished.')
                  
                countdown1()
                    
        countdown()    


@bot.event 
async def on_voice_state_update(member, before, after): #Удаляет войс 
   
    if g < 20000: # Если денег на Payment нет , - войс
        cchanelid = channelid
        channel = bot.get_channel(cchanelid)
        await channel.delete()


@bot.command() 
async def newrole(ctx, *,rolename=None): 
    connection = sqlite3.connect('bot_test.db')# Подключение к бд
    cursor = connection.cursor()
    rolepay = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]# Присваиваем переменную 
    op = int(rolepay)
    roleprice = 500000
    if op > 500000: # если денег хватает, идем дальше
        if not rolename:
            embed = discord.Embed(
            title="Введите название роли.",
            )
            await ctx.send(embed=embed)
        
        else:
            cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(roleprice, ctx.author.id))
            role = await ctx.guild.create_role(name=rolename, mentionable=True)
            cust = role
            await ctx.author.add_roles(role)
            embed = discord.Embed(
            title=f"Вы успешно создали роль. Для редакции роли обратитесь к @St1zy3"
            )
            await ctx.send(embed=embed)
            customrole = {role.mention}

    elif op < 500000: # Денег нехватает 
        embed = discord.Embed(
        title="Недостаточно средств.",
        )
        await ctx.send(embed=embed)

    


@bot.command() # Панель управления созданным войсом.
async def voicemenu(ctx):
    await ctx.send("Команды упавления личным голосовым чатом.") 




@bot.command()
async def payment(ctx, Oplata):
    # Также удалил поле time и добавил поле Payment в бд
    connection = sqlite3.connect('bot_test.db')# Подключение к бд
    cursor = connection.cursor()
    aoplata = int(Oplata)
    balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]# Присваиваем баланс из бд к переменной
    
    if balance >= aoplata:
        cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(aoplata, ctx.author.id)) # Вычитаем деньги за оплату войса
        cursor.execute("UPDATE users SET Payment = Payment + {} WHERE id = {}".format(aoplata, ctx.author.id)) # Пополняем поле Payment
        connection.commit()
        embed = discord.Embed(
        title="Оплата прошла успешно.",
        )
        await ctx.send(embed=embed) 
    elif balance < aoplata:
        await ctx.send("Недостаточно средств!")



bot.run(settings['token'])












