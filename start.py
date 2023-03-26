import daemon

from flask import main
from tg import bot

with daemon.DaemonContext():
    main.app.run()
    bot.start_bot()