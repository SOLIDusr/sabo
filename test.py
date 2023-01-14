from configs.database_config import *
from tools.logs import Log as logger
from tools.db_connect import cursor
from tools.db_request import Request

name = Request.Get.any('nickname', 'users', 'id', 442392434899681280)
print(name)
