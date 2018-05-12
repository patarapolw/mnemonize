import yaml
import string
import itertools
from diceware_utils.wordlist import Wordlist

from mnemonize.gibberish import Gibberish
from mnemonize.dir import database_path

NOT_CHARS = string.digits + string.punctuation


class Wordify:
    def __init__(self):
        self.desubstitutions = dict()

        with open(database_path('leetspeak.yaml')) as f:
            leetspeak = yaml.safe_load(f)
            for k, v in leetspeak['min'].items():
                for item in v:
                    if item in NOT_CHARS:
                        self.desubstitutions.setdefault(item, set()).add(k)
            for k, v in leetspeak['reverse'].items():
                if k in NOT_CHARS:
                    self.desubstitutions.setdefault(k, set()).add(v)

        with open(database_path('mnemonic.yaml')) as f:
            major_system = yaml.safe_load(f)['major_system']
            for k, v in major_system.items():
                if k in NOT_CHARS:
                    self.desubstitutions.setdefault(k, set()).update(v)

        assert set(NOT_CHARS) - set(self.desubstitutions.keys()) == set(), "Not all not chars are covered"

        dictionaries_to_include = ['aspell-en', 'cracklib-small', 'eff-long']
        self.dictionary = set(sum([Wordlist(dictionary).wordlist for dictionary in dictionaries_to_include], []))

        self.gibberish = Gibberish()

    def letterify(self, password):
        password_array = []
        for char in password.lower():
            if char not in string.ascii_lowercase:
                desub = list(self.desubstitutions[char])
                if None not in desub:
                    password_array.append(desub)
            else:
                password_array.append([char])
        return password_array

    def wordify(self, password, min_word_length=3):
        password_array = self.letterify(password)
        password_array_length = len(password_array)

        for length in reversed(range(min_word_length, password_array_length)):
            for i in range(password_array_length - length + 1):
                words = password_array[i:i+length]
                dictionary_word = self.in_dictionary(words)
                if dictionary_word is not None:
                    password_array = self.alter_list(password_array, i, dictionary_word)

        for length in reversed(range(min_word_length, password_array_length)):
            for i in range(password_array_length - length + 1):
                words = password_array[i:i+length]
                gibberish_word = self.gibberish.in_gibberish(words)
                if gibberish_word is not None:
                    password_array = self.alter_list(password_array, i, gibberish_word)

        for length in (2, 1):
            for i in range(password_array_length - length + 1):
                pre_gibberrish = password_array[i:i+length]
                gibberish_word = self.gibberish.to_gibberish(pre_gibberrish)
                if gibberish_word is not None:
                    password_array = self.alter_list(password_array, i, gibberish_word, length=length)

        return [char_array[0] for char_array in password_array if char_array != []]

    def in_dictionary(self, words):
        word_list = [''.join(letters) for letters in itertools.product(*words)]

        for word in word_list:
            if word in self.dictionary:
                return word

        return None

    @staticmethod
    def alter_list(password_array, i, dictionary_word, length=None):
        password_array[i] = [dictionary_word]

        if length is None:
            length = len(dictionary_word)
        for x in range(1, length - 1):
            password_array[i + x] = []

        return password_array


if __name__ == '__main__':
    print(Wordify().wordify('Re\'BlankRe*o{S25E'))
