from time import sleep

from src.components.convert import convert_to_acres99_dict
from src.components.fetch import response
from src.entity import Acres99


def main():
    for i in range(5):
        r = response(i, 800)
        acres99_dict = convert_to_acres99_dict(r.json())

        acres = Acres99(**acres99_dict)
        acres.export_dfs(drop_duplicates=True)
        sleep(5)


if __name__ == '__main__':
    main()
