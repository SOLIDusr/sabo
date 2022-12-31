import discord
from discord.ext import commands
from configs.config import *
import time
import math
import os
from logs import logger, handler
import psycopg2 as sql
from configs.database_config import *



intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, help_command=None)


global payment1
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

    logger.info(f'Error happend while connecting to Database! {Exception}')


# bot.event
@bot.event
async def on_ready():
    logger.info("Bot started")
    logger.info(f"Bot name is {bot.user.name}")
    logger.info(f'Client id is {bot.user.id}')
    global tdict
    tdict = {}
    await bot.add_cog(CommandsVoice())
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


@bot.event  # Узнает время в войсе
async def on_voice_state_update(member, before, after):
    payment2 = int(payment1)

    if payment2 < 12000:  # Если денег на Payment нет , - войс

        cchanelid = channelid
        channel = bot.get_channel(cchanelid)
        await channel.delete()

    else:

        pass

    author = member.id

    if before.channel is None and after.channel is not None:

        t1 = time.time()
        tdict[author] = t1

    elif before.channel is not None and after.channel is None and author in tdict:

        t2 = time.time()
        t3 = t2 - tdict[author]
        tround = math.ceil(t3)
        vtim = tround / 60
        vtime = math.ceil(vtim)

        if vtime <= 1:  # Проверка на время в войсе (Менее одной минуты или нет)

            pass

        elif vtime > 1:

            vtimer = vtime * 10  # Начисление за проведенный промежуток времени

            cursor.execute(f'SELECT money FROM users where id={member.id}')
            row = cursor.fetchone()
            cursor.execute(f'UPDATE users SET money={vtimer + row[0]} where id={member.id}')

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


class CommandsVoice(commands.Cog):
    def __init__(self):
        self.bot = bot

    @commands.command()
    async def create_voice(self, ctx, channel_name):
        cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id))  # Присваиваем баланс из бд к переменной
        balance = cursor.fetchone()[0]
        purchase = 2500

        if balance < purchase:

            he1 = discord.Embed(title="[Payment]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
            await ctx.send(embed=he1)

        elif balance >= purchase:

            cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(purchase, ctx.author.id))
            data_base.commit()
            guild = ctx.guild
            channel = await guild.create_voice_channel(channel_name)
            connected = ctx.author.voice
            channel = discord.utils.get(ctx.guild.channels, name=channel_name)
            channelid = channel.id
            print(channelid)
            he1 = discord.Embed(title="[VoiceManager]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Голосовой канал создан.',
                          value="У вас есть 24 часа для того чтобы оплатить голосовой канал, иначе он будет удален.",
                          inline=False)
            he1.add_field(name='Управление каналом.', value="/voicemenu", inline=False)
            he1.add_field(name='Помощь с личным каналом.', value="/voicehelp", inline=False)
            await ctx.send(embed=he1)
            pay = 12000  # Сумма которая будет отниматься за недельную оплату

            def countdown(

                    num_of_secs=86400):  # таймер, количество секунд (num_of_secs), до которого будет отсчитывать
                # таймер (24 часа). (86400)

                while num_of_secs:  # Переменная num_of_secs будет непрерывно уменьшаться в цикле, пока не достигнет
                    # 0 (что переводится в False и завершает цикл без каких-либо дополнительных условий).

                    m, s = divmod(num_of_secs,
                                  60)  # Функция divmod принимает два числа и возвращает произведение и остаток от
                    # двух чисел.
                    min_sec_format = '{:02d}:{:02d}'.format(m, s)
                    time.sleep(1)
                    num_of_secs -= 1
                print('Countdown finished.')
                cursor.execute("SELECT Payment FROM users WHERE id = {}".format(ctx.author.id)) # Присваиваем переменную
                payment = cursor.fetchone()[0]
                payment1 = int(payment)

                if payment1 >= 12000:  # Если в поле Payment есть 12000, войс продляется на 7 дней

                    cursor.execute("UPDATE users SET Payment = Payment - {} WHERE id = {}".format(pay, ctx.author.id))

                    def countdown1(num_of_secs=604800):

                        while num_of_secs:

                            m, s = divmod(num_of_secs, 60)
                            min_sec_format = '{:02d}:{:02d}'.format(m, s)
                            time.sleep(1)
                            num_of_secs -= 1
                        print('Countdown finished.')

                    countdown1()

            countdown()

    @commands.command()
    async def voicemenu(self, ctx):
        he1 = discord.Embed(title="Команды упавления личным голосовым чатом.", colour=discord.Colour(0x3e038c))
        he1.add_field(name='/lock', value="Закрывает доступ к комнате.", inline=False)
        he1.add_field(name='/open', value="Открывает доступ к комнате.", inline=False)
        await ctx.send(embed=he1)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.purge(limit=1)
        channel = ctx.message.author.voice.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.connect = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def open(self, ctx):
        await ctx.channel.purge(limit=1)
        channel = ctx.message.author.voice.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.connect = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    @commands.command
    async def payment(self, ctx, Oplata):
        aoplata = int(Oplata)
        cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id))
        balance = cursor.fetchone()[0]

        if balance >= aoplata:

            cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(aoplata, ctx.author.id))
            cursor.execute("UPDATE users SET Payment = Payment + {} WHERE id = {}".format(aoplata, ctx.author.id))
            data_base.commit()
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

    #
    #---------------ФРАГМЕНТ КОДА ДЛЯ БУДУЩЕЙ РЕАЛИЗАЦИИ!!!----------------------------------
    # @bot.command(name="kick", pass_context=True)
    # @has_permissions(manage_roles=True, ban_members=True)
    # async def _kick(ctx, member: discord.Member):
    #     await bot.kick(member)
    #
    # @_kick.error
    # async def kick_error(ctx, error):
    #     if isinstance(error, MissingPermissions):
    #         text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    #         await bot.send_message(ctx.message.channel, text)
    #
    #
    #

bot.run(settings['token'], log_handler=handler)
