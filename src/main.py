import asyncio

from src.components.convert import convert_to_acres99_dict
from src.components.fetch import response
from src.database.operation import DataFrameOperations, DFPath
from src.entity import Acres99

PAGE_NUMBERS = range(20, 40)
PROP_PER_PAGE = 500


async def get_acres99_obj(page_num: int, page_size: int) -> Acres99:
    data = await response(page_num, page_size)

    if isinstance(data, dict):
        acres99_dict = await convert_to_acres99_dict(data)
        acres = Acres99(**acres99_dict)
        return acres
    else:
        raise RuntimeError('Response data is not dict data type.')


async def export_srp_df(pages: list[int] | range, prop_per_page: int) -> None:
    for i in pages:
        acres99 = await get_acres99_obj(i, prop_per_page)
        df_op = DataFrameOperations(acres99)

        await df_op.export_df(await acres99.to_df('srp'), DFPath.srp)

    await DataFrameOperations.drop_duplicates(DFPath.srp)


async def main():
    await export_srp_df(PAGE_NUMBERS, PROP_PER_PAGE)


if __name__ == '__main__':
    asyncio.run(main())
