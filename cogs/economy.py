import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from tools.logs import Log as logger
from tools.db_connect import cursor
from tools.db_request import Request
from main import bot


# cursor.execute(f'SELECT prefix FROM guilds WHERE id = 780063558482001950')
# prefix = cursor.fetchone()[0]
# intents = discord.Intents.all()
# bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)


class Economics(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['bal', 'баланс', 'бал'])
    async def balance(self, ctx, member: discord.Member = None):

        if member is not None:

            try:
                
                try:
                    
                    name, balance = Request.Get.name(member.id), Request.Get.balance_by_id(member.id)
                    if type(name) is Exception or type(balance) is Exception:
                        logger.error(f'SQL request Error:\n{name, balance}')
                        ctx.send('Извините, произошла ошибка. Свяжитесь с администратором сервера.')
                    else:
                        pass
                
                except Exception as _ex:

                    logger.error(f'SQL request Error:\n{_ex}')
                    ctx.send('Извините, произошла ошибка. Свяжитесь с администратором сервера.')

                if name is None:

                    logger.info(f'money command error: {error}')
                    embed = discord.Embed(title='Оповещение', color=0xFF0000)
                    embed.add_field(name='Оповещение', value='Ошибка при выполнение программы.')
                    await ctx.send(embed=embed) 
                
                else:

                    embed = discord.Embed(title=f'Аккаунт пользователя {name}', color=0x42f566)
                    embed.add_field(name='Баланс:', value=f'{balance} SH', inline=False)
                    await ctx.send(embed=embed)

            except Exception as error:

                logger.info(f'money command error: {error}')
                embed = discord.Embed(title='Оповещение', color=0xFF0000)
                embed.add_field(name='Оповещение', value='Ошибка при выполнение программы.')
                await ctx.send(embed=embed)

        elif member is None:
            member = ctx.author
            balance = Request.Get.balance_by_id(member.id)
            embed = discord.Embed(title=f'Аккаунт пользователя {member.name}', color=0x42f566)
            embed.add_field(name='Баланс:', value=f'{balance} SH', inline=False)
            await ctx.send(embed=embed)


    @commands.command(name="set_money", pass_context=True)
    @has_permissions(manage_roles=True, ban_members=True)
    async def set_money(self, ctx, member: discord.Member, amount: int = None):

        if amount < 0:

            await ctx.send('Количество не может быть отрицательным!')

        else:
            response = Request.Set.balance_by_id(member.id, amount)
            if response is True:
                embed = discord.Embed(title='Пополнение баланса', color=0x42f566)
                embed.set_author(name='Community Bot')
                embed.add_field(name='Оповещение', value=f'Баланс пользователя {member.name} пополнен на {amount} SH')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='Пополнение баланса', color=0x42f566)
                embed.set_author(name='Community Bot')
                embed.add_field(name='Оповещение', value=f'Произошла ошибка! Подробности смотрите в логгах')
                await ctx.send(embed=embed)
                logger.error(f'Error in set_money. Error:\n{response}')


    @set_money.error
    async def set_money_error(self, ctx, error):

        if isinstance(error, MissingPermissions):
            text = "Извините {}, У вас нет полномочий на это!".format(ctx.message.author)
            await ctx.send(ctx.message.channel, text)


    @commands.command(aliases=['prof', 'профиль', 'p'])
    async def profile(self, ctx, member: discord.Member = None):
        
        if member is None:
            member = ctx.author

        nickname = member.name
        balance = Request.Get.balance_by_id(member.id)
        discord_channel_id = Request.Get.channel_discord_by_owner(member.id)
        if balance is Exception or discord_channel_id is Exception:
            logger.error(f'Error in economics on lines 108- 109. Error:\n{balance, discord_channel_id}')
            ctx.send('Ошибка выполнения команды! Свяжитесь с администратором.')

        elif discord_channel_id is None:
            
            channelz = 'Не найдено'
            logger.info(discord_channel_id)

        else:

            channelz = f'<#{discord_channel_id[0]}>'
            
        embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f'{member}')
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f'Запрошено пользователем - {ctx.author}', icon_url=ctx.author.avatar.url)
        embed.add_field(name='Имя:👤', value=nickname, inline=False)
        embed.add_field(name='Баланс:🪙', value=balance, inline=False)
        embed.add_field(name='Роль:🛡', value=member.top_role.mention, inline=False)
        embed.add_field(name='Присоеденился к Discord:🕔', value=member.created_at, inline=False)
        embed.add_field(name='На сервере с:🕔', value=member.joined_at, inline=False)
        embed.add_field(name='Voice Room:🕪', value=f'{channelz}', inline=False)

        await ctx.send(embed=embed) 

# noinspection PyShadowingNames
async def setup(bot):
    await bot.add_cog(Economics())
