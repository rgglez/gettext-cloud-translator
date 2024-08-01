from rich.pretty import pprint
from config_chatgpt import ChatGptConfiguration

class TranslatorFactory:
    @staticmethod
    def create_translator(args):
        if args.backend == "chatgpt":
            from translator_chatgpt import TranslatorChatGPT
            from config_chatgpt import ChatGptConfiguration
            return TranslatorChatGPT(ChatGptConfiguration(args))
        elif args.backend == "azure":            
            from translator_azure import TranslatorAzure
            from config_azure import AzureConfiguration
            return TranslatorAzure(AzureConfiguration(args))
        else:
            raise ValueError("Unknown translation backend")
# TranslatorFactory