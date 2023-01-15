import discord
from tools.logs import Log as logger
from tools.db_connect import cursor
from tools.db_request import Request
from datetime import datetime as nowadays


class Gamble():

    def __init__(self) -> None:
        pass

    def bet(member: discord.Member, value, comment:str = None) -> bool | Exception:
        try:
            id = member.id
            Request.Update.balance(id=id, adding=-value)
            logger.info(f'{member} made a bet on {value}. '+ comment)
            return True
        except Exception as _ex:
            return _ex
    
    def loose(member: discord.Member) -> None:
        logger.info(f'{member} lost his bet')

    def win(member:discord.Member, value, comment:str = None) -> bool | Exception:
        try:
            id = member.id
            Request.Update.balance(id=id, adding=value)
            logger.info(f'{member} won {value}. '+ comment)
            return True
        except Exception as _ex:
            return _ex