from diceware_utils.generate import GeneratePassword


if __name__ == '__main__':
    gp = GeneratePassword()
    for _ in range(50):
        print(gp.generate())
