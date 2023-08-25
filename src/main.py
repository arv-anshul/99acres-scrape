import asyncio

from src.components import convert, fetch
from src.database.operation import DataFrameOperations, DFPath
from src.entity import Acres99

PAGE_NUMS = range(1, 20)
PROP_PER_PAGE = 500


async def export_srp_df(
    page_nums: list[int] | range,
    prop_per_page: int,
    city_id: int | None = None,
) -> None:
    responses = await fetch.fetch_all_responses(list(page_nums), prop_per_page, city_id=city_id)
    data = await convert.concat_responses(responses)
    acres99 = Acres99(**data)

    df_op = DataFrameOperations(acres99)

    await df_op.export_df(await acres99.to_df('srp'), DFPath.srp)
    await DataFrameOperations.drop_duplicates(DFPath.srp)


async def main():
    await export_srp_df(PAGE_NUMS, PROP_PER_PAGE)


if __name__ == '__main__':
    asyncio.run(main())
