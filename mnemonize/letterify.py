import yaml
import string

from mnemonize.dir import database_path

NOT_CHARS = string.digits + string.punctuation


class Letterify:
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


if __name__ == '__main__':
    print(Letterify().letterify('Re\'BlankRe*o{S25E'))
