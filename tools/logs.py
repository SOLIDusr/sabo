import logging


class CustomFormatter(logging.Formatter):
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s][%(levelname)s] %(message)s"
    
    FORMATS = {
        logging.DEBUG: format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.FATAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


Log = logging.getLogger()
Log.setLevel(logging.INFO)
Channel = logging.StreamHandler()
Channel.setLevel(logging.INFO)
Channel.setFormatter(CustomFormatter())
Log.addHandler(Channel)
logging.basicConfig(filename='logfile.log', encoding='utf-8', level=logging.DEBUG)