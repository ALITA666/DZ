from data.config import Tokens
from utils.bot import GroupBot
from handlers import bps

bot = GroupBot(token=Tokens.group)

for bp in bps:
    bp.load(bot)

bot.run_forever()
