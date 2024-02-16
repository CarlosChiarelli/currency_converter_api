from asyncio import gather
from typing import Coroutine, List

from converter import async_converter, sync_converter  # type: ignore
from fastapi import APIRouter, Path, Query
from schemas import ConverterInput, ConverterOutput  # type: ignore

router = APIRouter(prefix="/converter")


@router.get("/{from_currency}", response_model=ConverterOutput)
def converter(
    from_currency: str = Path(max_length=3, regex="^[A-Z]{3}$"),
    to_currencies: str = Query(max_length=50, regex="^[A-Z]{3}(,[A-Z]{3})*$"),
    price: float = Query(gt=0),
) -> ConverterOutput:
    to_currencies_list: List[str] = to_currencies.split(",")

    result: List[dict] = []

    for currency in to_currencies_list:
        response: dict = sync_converter(
            from_curency=from_currency, to_currency=currency, price=price
        )

        result.append(response)

    return ConverterOutput(message="success", data=result)


@router.get("/async/{from_currency}", response_model=ConverterOutput)
async def async_converter_router(
    from_currency: str = Path(max_length=3, regex="^[A-Z]{3}$"),
    to_currencies: str = Query(max_length=50, regex="^[A-Z]{3}(,[A-Z]{3})*$"),
    price: float = Query(gt=0),
) -> ConverterOutput:
    to_currencies_list: List[str] = to_currencies.split(",")

    couroutines: List[Coroutine] = []

    for currency in to_currencies_list:
        coro: Coroutine = async_converter(
            from_curency=from_currency, to_currency=currency, price=price
        )

        couroutines.append(coro)

    result: List[dict] = await gather(*couroutines)

    return ConverterOutput(message="success", data=result)


@router.get("/async/v2/{from_currency}", response_model=ConverterOutput)
async def async_converter_router_v2(
    body: ConverterInput, from_currency: str = Path(max_length=3, regex="^[A-Z]{3}$")
) -> ConverterOutput:
    to_currencies_list: List[str] = body.to_currencies
    price: float = body.price

    couroutines: List[Coroutine] = []

    for currency in to_currencies_list:
        coro: Coroutine = async_converter(
            from_curency=from_currency, to_currency=currency, price=price
        )

        couroutines.append(coro)

    result: List[dict] = await gather(*couroutines)

    return ConverterOutput(message="success", data=result)
