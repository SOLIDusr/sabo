import discord
from discord.ext import commands
from discord.ui import Button, View
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


class Roles(commands.Cog):
    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['rolebuy', 'buyrole'])
    async def _rolebuy(self, ctx, num:int = None):

        cursor.execute(f'SELECT id FROM roles_shop')
        idss = cursor.fetchall()
        member:discord.Member = ctx.author
        ids = []
        for id in idss:
            ids.append(id[0])

        if num is None:

            ctx.send('Вы не ввели обязательный параметр числа!')

        elif num not in ids:

            he1 = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Ошибка!', value="Используйте правильный номер роли.", inline=False)
            he1.add_field(name='Покупка', value="/role купить", inline=False)
            await ctx.send(embed=he1)

        else:

            cursor.execute(f'SELECT role_cost, discord_id FROM roles_shop WHERE id = {num}')
            row = cursor.fetchone()
            role_cost, discord_id = row[0], row[1]
            cursor.execute(f'SELECT money FROM users WHERE id = {ctx.author.id}')
            balance = cursor.fetchone()[0]

            if balance < role_cost:

                he1 = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Спасибо за покупку!',
                            value="Хотелось бы так сказать, но у вас не хватило средств :(.",
                            inline=False)
                await ctx.send(embed=he1)
            
            elif discord_id in member.roles:
                he1 = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Спасибо за покупку!',
                            value="Хотелось бы так сказать, но у вас уже есть эта роль :)   .",
                            inline=False)
                await ctx.send(embed=he1)
            else:
                user: discord.Member = ctx.author
                cursor.execute(f'UPDATE users SET money = money - {role_cost} WHERE id={ctx.author.id}')
                role = discord.utils.get(ctx.guild.roles, id=discord_id)
                await user.add_roles(role)
                
                data_base.commit()
                he1 = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Вниание!', value="Система искренне завидует вашей покупке.", inline=False)
                await ctx.send(embed=he1)

    @commands.command(aliases=['role', 'roles', 'роль', 'роли'])  # создание роли
    async def _role(self, ctx, move:str = None):
        
        moves = ['купить', 'покупка', 'buy', 'shop', 'магазин']
        
        if move is None:

            async def custom_role_shop():

                await ctx.send('Введите "/custom {имя роли} {Цвет Роли}" чтобы создать свою роль.')

            async def existing_role_shop():
                embi = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
                embi.add_field(name='', value="Выберите интересующую вас роль.", inline=False)
                cursor.execute(f'SELECT id FROM roles_shop')
                choise_ids = cursor.fetchall()

                for item in choise_ids:
                    
                    cursor.execute(f"SELECT role_cost FROM roles_shop WHERE id = {item[0]}")
                    choise_cost = cursor.fetchone()[0]
                    cursor.execute(f'SELECT role_name FROM roles_shop WHERE id = {item[0]}')
                    name = cursor.fetchone()[0]

                    embi.add_field(name=f'Роль №{item[0]} - {name}', value=f'Цена - {choise_cost} SH',
                                   inline=False)
                embi.add_field(name='Для покупки напишите', value='/rolebuy [id роли]')
                await ctx.send(embed=embi)

            # Ответы от нажатий кнопок

            async def custom_role_call(inter):
                await inter.response.defer()
                await custom_role_shop()

            async def buyrole_call(inter):
                await inter.response.defer()
                await existing_role_shop()

            emb = discord.Embed(title='[RoleShop]',
                                description="Тут вы можете купить индивидуальную роль с помощью виртуальной "
                                            "валюты.", colour=discord.Colour.purple())
            emb.add_field(name='RoleShop', value='Все категории представлены ниже', inline=False)
            roles_b = Button(label='Досупные роли', style=discord.ButtonStyle.primary, emoji='👑')
            custom_role_b = Button(label='Личная роль', style=discord.ButtonStyle.primary,
                                   emoji='<:booster:1029482318118797412>')

            custom_role_b.callback = custom_role_call
            roles_b.callback = buyrole_call
            view = View()
            view.add_item(custom_role_b)
            view.add_item(roles_b)

            await ctx.send(embed=emb, view=view)

    @commands.command(aliases=['customize', 'custom', 'кастом', 'customise'])
    async def _custom(self, ctx, role_name:str = None, role_colour:discord.Color = None):
        member: discord.Member = ctx.author

        FORBIDDEN = ['staff', 'dev', 'developer', 'devops', 'admin', 'admins', 'moderator', 'mods', 'moder', 'mod', 'owner', 'robot',
                    'headquaters', 'event mod', 'booster', 'the chosen one [Tier-5]', 'protector [Tier-4], duelist [Tier-3]']

        if role_colour is None:

            role_colour = member.color

        colours = ['red', 'purple', 'green', 'blue']

        cursor.execute(f'SELECT money FROM users WHERE id = {ctx.author.id}')
        balance = cursor.fetchone()[0]

        if (role_name is None or role_colour is None or role_colour not in colours) or len(role_name) >= 16 or role_name.lower in FORBIDDEN:

            embi = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
            embi.add_field(name='', value="Неправильно указаны цвет или имя роли!.", inline=False)
            embi.add_field(name='Пример', value="/custom {Имя роли} {Цвет Роли}!.", inline=False)
            embi.add_field(name='Цвета', value="красный - red\n\nфиолетовый - purple\nСиний -  blue\nЗеленый - green.", inline=False)
            await ctx.send(embed=embi)

        elif balance < 5_500_000:

            embi = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
            embi.add_field(name='Недостаточно средств!', value=f"Не хватает - {500_000 - balance}", inline=False)
            await ctx.send(embed=embi)
        
        else:

            guild = ctx.guild
            cursor.execute(f'UPDATE users SET money = money - 5500000 WHERE id = {ctx.author.id}')
            role = await guild.create_role(name=role_name, colour=role_colour, hoist=True, mentionable=True)
            await member.add_roles(role)
            emb=discord.Embed(
                title='Создание Личной Роли',
                description=f'{ctx.author.mention}, вы успешно **создали** роль {role.mention}.'
            )
            emb.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=emb)
            positions = {
                role: 11
            }
            await guild.edit_role_positions(positions=positions)



# noinspection PyShadowingNames
async def setup(bot):
    await bot.add_cog(Roles())
