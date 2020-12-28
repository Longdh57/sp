import random
import string
import faker.providers


class UtilProvider(faker.providers.BaseProvider):
    @staticmethod
    def string(length=10, uppercase=False, digits=False):
        letters = string.ascii_uppercase if uppercase else string.ascii_lowercase
        letters += string.digits if digits else ''
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def phone_number():
        """
        Random a phone number with format "84xxx"
        :return:
        """
        return '849' + ''.join([random.choice('0123456789') for _ in range(8)])
