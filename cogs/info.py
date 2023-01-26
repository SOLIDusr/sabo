import discord
from discord.ui import Button, View
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from tools.logs import Log as logger
from tools.db_connect import cursor
from tools.db_request import Request

bot = Request.get_bot()

class Info(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['помощь', 'help', 'справка', '?'])
    async def _help(self, ctx):

        page = 0

        async def go_back(inter):
            await inter.response.defer()

            if page == 0:

                starterpage=discord.Embed(title="", description="", color=0xf00000)
                starterpage.set_author(name="**[НАЧАЛО]**")
                starterpage.set_thumbnail(url="https://wallpaperaccess.com/full/6999296.jpg")
                starterpage.add_field(name="Информация", value="Текст", inline=True)
                starterpage.set_footer(text=f"Страница номер {page}")
                previous_page = Button(label='', style=discord.ButtonStyle.primary, emoji='⬅️')
                next_page = Button(label='', style=discord.ButtonStyle.primary,
                                        emoji='➡️')

                previous_page.callback = go_back
                next_page.callback = go_next
                view = View()
                view.add_item(previous_page)
                view.add_item(next_page)
    
                await ctx.edit(embed=starterpage, view = view, ephemeral=True)
                
    
        async def go_next(inter):
            await inter.response.defer()
            if page == 0:
                page += 1
                await currency()


        async def currency():
            starterpage=discord.Embed(title="ava", description="afa", color=0xf00000)
            starterpage.set_author(name="**[ВАЛЮТА]**")
            starterpage.set_thumbnail(url="https://wallpaperaccess.com/full/6999296.jpg")
            starterpage.add_field(name="Информация", value="Текст", inline=True)
            starterpage.set_footer(text=f"Страница номер {page}")
            previous_page = Button(label='', style=discord.ButtonStyle.primary, emoji='⬅️')
            next_page = Button(label='', style=discord.ButtonStyle.primary,
                                    emoji='➡️')

            previous_page.callback = go_back
            next_page.callback = go_next
            view = View()
            view.add_item(previous_page)
            view.add_item(next_page)
            await ctx.edit(embed=starterpage, view = view, ephemeral=True)


        starterpage=discord.Embed(title="", description="", color=0xf00000)
        starterpage.set_author(name="**[НАЧАЛО]**")
        starterpage.set_thumbnail(url="https://wallpaperaccess.com/full/6999296.jpg")
        starterpage.add_field(name="Информация", value="Текст", inline=True)
        starterpage.set_footer(text=f"Страница номер {page}")
        previous_page = Button(label='', style=discord.ButtonStyle.primary, emoji='⬅️')
        next_page = Button(label='', style=discord.ButtonStyle.primary,
                                emoji='➡️')

        previous_page.callback = go_back
        next_page.callback = go_next
        view = View()
        view.add_item(previous_page)
        view.add_item(next_page)
        
        msg = await ctx.send(embed=starterpage, view = view, ephemeral=True)
        
    @commands.command(aliases=['stat', 'статы'])
    async def stats(self, ctx):
        embed=discord.Embed(title="Рейтинг по уровню", color=0xe70404)
        embed.set_author(name=f"Топ 10 сервера...")
        embed.set_author(name=f"Загрузка... ")
        msg = await ctx.send(embed=embed)
        lvl_top = {}
        
        cursor.execute('SELECT nickname, lvl FROM users ORDER BY -lvl')
        levels = cursor.fetchall()

        if levels is Exception:
            logger.error(levels)
            quit(-1)

        else:
            pass
            
        for data in levels:
            lvl_top[data[0]] = data[1]  
            cursor.execute(f"SELECT voicetime FROM users WHERE nickname = '{data[0]}'")
        lenlist = 10
        if len(lvl_top) < 10:
            lenlist = len(lvl_top)

        embed=discord.Embed(title="Рейтинг по уровню", color=0xe70404)
        embed.set_author(name=f"Топ {lenlist} сервера")
        for i in range(lenlist):
            if i == 0:
                embed.add_field(name=f"#{i + 1}🥇 {list(lvl_top.keys())[i]}", value=f"**Уровень**:🏆 {list(lvl_top.values())[i]}", inline=False)
            elif i ==1:
                embed.add_field(name=f"#{i + 1}🥈 {list(lvl_top.keys())[i]}", value=f"**Уровень**:🏆 {list(lvl_top.values())[i]}" , inline=False)
            elif i == 2:
                embed.add_field(name=f"#{i + 1}🥉 {list(lvl_top.keys())[i]}", value=f"**Уровень**:🏆 {list(lvl_top.values())[i]}", inline=False)
            else:
                embed.add_field(name=f"#{i + 1} {list(lvl_top.keys())[i]}", value=f"**Уровень**:🏆 {list(lvl_top.values())[i]}", inline=False)

        embed.set_footer(text=f"Запросил {ctx.author.name}")
        await msg.edit(embed=embed)


        # noinspection PyShadowingNames
async def setup(bot):
    await bot.add_cog(Info())

    #  доделать функцию
