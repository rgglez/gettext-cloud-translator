from abc import ABC, abstractmethod

###############################################################################

class TranslatorService(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass
    # __init__

    @abstractmethod
    def translate_in_bulk(self, texts):
        pass
    # translate_in_bulk
        
    @abstractmethod
    def translate_one_by_one(self, texts):
        pass
    # translate_one_by_one    
# TranslatorService