import asyncio

from src.components import convert, fetch
from src.database.operation import DataFrameOperations, DFPath
from src.entity import Acres99

PAGE_NUMS = range(1, 20)
PROP_PER_PAGE = 500


async def get_acres99_obj(page_nums: list[int], prop_per_page: int) -> Acres99:
    responses = await fetch.fetch_all_responses(page_nums, prop_per_page)
    data = await convert.concat_responses(responses)
    acres = Acres99(**data)
    return acres


async def export_srp_df(page_nums: list[int] | range, prop_per_page: int) -> None:
    acres99 = await get_acres99_obj(list(page_nums), prop_per_page)
    df_op = DataFrameOperations(acres99)

    await df_op.export_df(await acres99.to_df('srp'), DFPath.srp)
    await DataFrameOperations.drop_duplicates(DFPath.srp)


async def main():
    await export_srp_df(PAGE_NUMS, PROP_PER_PAGE)


if __name__ == '__main__':
    asyncio.run(main())
