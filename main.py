import discord
from discord.ext import commands
import os
from tools.logs import Log as logger
from tools.db_connect import cursor
from tools.db_request import Request
from tools.plugins import *


try:
    
    try:
        token = Request.Get.any('token', 'guilds', 'id', '780063558482001950')
        bot = Request.get_bot()
        if type(bot) is Exception:
            logger.critical(f'Could\'nt receve bot variable. Error:\n{bot}')
            raise discord.errors.DiscordException
        else:
            pass

        if type(token) is not str:
            logger.error(f'Unable to receve a token. Error:\n{token}')
            raise discord.errors.ClientException
            
    except(Exception) as _ex:
        logger.error(f'Unable to receve a token. Error:\n{_ex}')


    # bot.event
    @bot.event
    async def on_ready():
        
        for filename in os.listdir("./cogs"):  # перебирает все файлы в выбранной папке
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")  # загрузка КОГов в основной файл
                logger.info(f'Extension {filename} loaded')
            else:
                logger.debug(f'Unexpected file {filename} in ./cogs folder')

        for guild in bot.guilds:
            logger.info(f'Connected to server, id is: {guild.id}')
            logger.warning(f'Wait until database fully fetched')

            for member in guild.members:
        
                cursor.execute(f"SELECT exists(select from users where id = {member.id})")
                if cursor.fetchone() is False:
                    cursor.execute(
                        f"INSERT INTO users (id, nickname, mention, money) VALUES ({member.id},"
                        f" '{member.name}', '<@{member.id}>', 0)")
                    logger.info(f'Added user to database')
                else:
                    pass

            logger.info('Database Full')

        logger.info(f"{bot.user.name} started on id {bot.user.id}")
        await bot.change_presence(activity=discord.Game('/help'))

    @bot.event
    async def on_member_join(member):

        logger.info(f'Member joined. Member - {member}')
        cursor.execute(f"SELECT exists(select from users where id = {member.id})")

        if cursor.fetchone() is False:
            cursor.execute(
                f"INSERT INTO users (id, nickname, mention, money) VALUES ({member.id},"
                f" '{member.name}', '<@{member.id}>', 0)")
            logger.info(f'Added user to database')


    @bot.command()
    async def plugin(ctx, todo: str = None):
        response = await manage_plugins(ctx, bot, todo)
        if response is True:
            pass
        else:
            logger.error(f'Plugins load failure! Exeption is: \n{response}')

    bot.run(token, log_handler=None)

except KeyboardInterrupt:
    logger.info('Shutting down bot')
    exit(0)

except Exception as _ex:
    logger.fatal('Unable to start the bot!')
    logger.fatal(_ex)
    exit(-1)