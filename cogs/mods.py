import discord
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ui import Select, View
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


class Moderation(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=["питомцы", "кейс с питомцами", "питомец кейс"])
    @has_permissions(manage_roles=True, ban_members=True)
    async def kick(self, ctx, intruder: discord.Member = None, reason: str = None):
        if intruder is None:
            await ctx.send('Не указан участник для кика.')
        else:
            await bot.kick(intruder)
            if reason is not None:
                await ctx.send(f'Участник {intruder} был выгнан с сервера участником {ctx.message.author} по причине'
                               f' {reason}.')


@bot.command(name="kick", pass_context=True)
async def _kick(ctx, member: discord.Member):
    await bot.kick(member)


@_kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await bot.send_message(ctx.message.channel, text)


async def setup(bot):
    await bot.add_cog(Moderation())

