"""
Edited from https://github.com/greghaskins/gibberish
Python pseudo-word generator
Copyright (c) 2011-2012 Gregory Haskins, http://greghaskins.com
"""

import yaml
import string
import itertools
try:
    from secrets import choice
except ImportError:
    from random import choice

from mnemonize.dir import database_path


class Gibberish:
    def __init__(self):
        with open(database_path('word_components.yaml')) as f:
            components = yaml.safe_load(f)

        self.initial_consonants = list(set(string.ascii_lowercase) - set('aeiou')
                                       # remove those easily confused with others
                                       # - set('qxc')
                                       # add some crunchy clusters
                                       | set(sum(components['initials'], []))
                                       )

        self.final_consonants = list(set(string.ascii_lowercase) - set('aeiou')
                                     # remove the confusables
                                     # - set('qxcsj')
                                     # crunchy clusters
                                     | set(sum(components['finals'], []))
                                     )

        self.vowels = list(set(sum(components['vowels'], [])))

    def generate_word(self, start_vowel=False, end_vowel=False,
                      initials=None, vowels=None, finals=None):
        """Returns a random consonant-(vowel-consonant)*wc pseudo-word."""
        if initials is None:
            initials = self.initial_consonants
        if vowels is None:
            vowels = self.vowels
        if finals is None:
            finals = self.final_consonants

        if not start_vowel:
            letter_list = [initials]
        else:
            letter_list = [vowels, self.final_consonants]

        letter_list.extend([self.vowels, finals])

        if end_vowel:
            letter_list.pop()

        return ''.join(choice(s) for s in letter_list)

    def in_gibberish(self, words):
        word_list = [''.join(letters) for letters in itertools.product(*words)]

        for word in word_list:
            initial = self.get_initial(word)
            final = self.get_final(word)
            if all([char in 'aeiouy' for char in (set(word) - set(initial) - set(final))]):
                return word

        return None

    def to_gibberish(self, char_lists):
        if [] in char_lists or char_lists == []:
            return None
        for char_list in char_lists:
            for char in char_list:
                if len(char) >= 3:
                    return None

        if len(char_lists) == 1:
            initials = char_lists[0]
            finals = self.final_consonants + self.vowels
        else:
            initials, finals = char_lists

        is_vowel_initials = (set(initials) - set(self.vowels) == set())
        is_vowel_finals = (set(finals) - set(self.vowels) == set())

        if is_vowel_initials and is_vowel_finals:
            vowels = [''.join(letters) for letters in itertools.product(*char_lists)]
            return self.generate_word(start_vowel=True, end_vowel=True, vowels=vowels)
        elif is_vowel_initials:
            return self.generate_word(start_vowel=True, end_vowel=False, vowels=initials, finals=finals)
        elif is_vowel_finals == '':
            return self.generate_word(start_vowel=False, end_vowel=True, initials=initials, vowels=finals)
        else:
            return self.generate_word(start_vowel=False, end_vowel=False,
                                      initials=initials, finals=finals)

    def get_initial(self, word):
        initial = ''
        for char in word:
            if char not in 'aeiou' and char in string.ascii_letters:
                initial += char
            else:
                if initial in self.initial_consonants:
                    return initial
                else:
                    return ''

        return ''

    def get_final(self, word):
        final = ''
        for char in word[::-1]:
            if char not in 'aeiou' and char in string.ascii_letters:
                final += char
            else:
                if final in self.final_consonants:
                    return final[::-1]
                else:
                    return ''

        return ''
