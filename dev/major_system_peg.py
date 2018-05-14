import requests
from bs4 import BeautifulSoup
import json
from mnemonize.dir import database_path


def generate_file():
    r = requests.get("https://en.wikipedia.org/wiki/Mnemonic_major_system")
    soup = BeautifulSoup(r.text, "html.parser")
    tables = soup.find_all("table")
    with open("peg.txt", "w") as f:
        for table_id in (1, 2):
            for tr in tables[table_id].find_all("tr"):
                for td in tr.find_all("td"):
                    f.write(td.text)
                    f.write('\t')
                f.write('\n')


def generate_json():
    def insert_to_json():
        for oneth, content in enumerate(row.strip().split('\t')):
            if tenth < 0:
                key = "{}".format(oneth)
            else:
                key = "{}{}".format(tenth, oneth)
            if '[' not in content:
                json_output.setdefault(key, list()).append(content)

    json_output = dict()
    with open("peg.txt") as f:
        for i, row in enumerate(f):
            case = i % 4
            tenth = i//4 - 1
            if case == 0:
                pass
            else:
                insert_to_json()

    with open(database_path("peg.json"), 'w') as f:
        json.dump(json_output, f, indent=2)


def extend_json():
    pass


if __name__ == '__main__':
    generate_json()
