from config_abc import TranslatorConfiguration

###############################################################################

class AzureConfiguration(TranslatorConfiguration):
    def __init__(self, args) -> None:
        self.apikey = args.apikey
        self.location = args.location
        self.file = args.file
        self.bulk = args.bulk
        self.bulksize = 49500 if args.bulksize > 49500 else args.bulksize
        self.fuzzy = args.fuzzy
        self.srclang = args.srclang
        self.dstlang = args.dstlang
    # __init__    
# ChatGptConfiguration