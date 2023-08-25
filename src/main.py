import asyncio

from src.components.convert import convert_to_acres99_dict
from src.components.fetch import response
from src.database.operation import DataFrameOperations
from src.entity import Acres99

PAGES_LIST = [1, 2, 3]
MAX_PAGE_SIZE = 30


async def process_request(page_num: int, page_size: int):
    data = await response(page_num, page_size)

    if isinstance(data, dict):
        acres99_dict = await convert_to_acres99_dict(data)
        acres = Acres99(**acres99_dict)
        df_operation = DataFrameOperations(acres)
        await df_operation.export_dfs(drop_duplicates=True)
    else:
        raise RuntimeError('Response data is not dict data type.')


async def main():
    tasks = []
    for i in PAGES_LIST:
        task = process_request(i, MAX_PAGE_SIZE)
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
