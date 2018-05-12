from diceware_utils.generate import GeneratePassword

from mnemonize.wordify import Wordify

gp = GeneratePassword()
wordify = Wordify()


if __name__ == '__main__':
    for _ in range(1000):
        password = gp.generate()
        if password is not None:
            print(password)
            print(wordify.wordify(password))