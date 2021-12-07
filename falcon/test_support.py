import string
import random
from tasks.models import Priority, Status


class Random:
    @ staticmethod
    def string(length: int = 5):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @ staticmethod
    def alpha_only(length: int = 5):
        return ''.join(random.choices(string.ascii_letters, k=length))

    @ staticmethod
    def email():
        return Random.string(10)+"@redhat.com"

    @ staticmethod
    def priority():
        return random.choice(Priority)

    @ staticmethod
    def status():
        return random.choice(Status)
