from config_abc import TranslatorConfiguration

###############################################################################

class ChatGptConfiguration(TranslatorConfiguration):
    def __init__(self, args) -> None:
        self.apikey = args.apikey
        self.file = args.file
        self.model = args.model
        self.bulksize = 50 if args.bulksize > 50 else args.bulksize
        self.fuzzy = args.fuzzy
        self.srclang = args.srclang
        self.dstlang = args.dstlang
    # __init__    
# ChatGptConfiguration