from apis.socialMedia import SocialMedia
from utils.singleton import Singleton


class Facebook(SocialMedia, metaclass=Singleton):
    def add_account(self, account):
        pass

    def remove_account(self, account):
        pass

    def recover_posts(self):
        pass
