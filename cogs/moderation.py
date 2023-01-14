import discord
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands
import psycopg2 as sql
from configs.database_config import *
from tools.logs import Log as logger


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
    exit()


cursor.execute(f'SELECT prefix FROM guilds WHERE id = 780063558482001950')
prefix = cursor.fetchone()[0]
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

class Moderation(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=["kick", "кик", "выгнать"])
    @has_permissions(manage_roles=True, ban_members=True)
    async def _kick(self, ctx, intruder: discord.Member = None, reason: str = None):
        if intruder is None:
            await ctx.send('Не указан участник для кика.')
        else:
            await intruder.kick()
            if reason is not None:
                await ctx.send(f'Участник {intruder} был выгнан с сервера участником {ctx.message.author} по причине'
                               f' {reason}.')

    @_kick.error
    async def _kick_error(ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await bot.send_message(ctx.message.channel, text)
    
    @commands.command(aliases=["jackpot", "kush", "куш"])
    @has_permissions(ban_members=True)
    async def _jackpot(self, ctx, amount):
        cursor.execute(f"UPDATE guilds SET jackpot = {amount} WHERE id = 780063558482001950")
        await ctx.send('Jackpot был изменен!')

# noinspection PyShadowingNames
async def setup(bot):
    await bot.add_cog(Moderation())

