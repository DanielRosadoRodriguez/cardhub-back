from abc import ABC, abstractmethod


class Dao(ABC):
    @abstractmethod
    def get():
        pass
    
    @abstractmethod
    def get_all():
        pass
    
    @abstractmethod
    def save():
        pass

    @abstractmethod
    def update():
        pass
    
    @abstractmethod
    def delete():
        pass
