import typing

T = typing.TypeVar('T')


def listify(obj: T) -> T | list[T]:
    if isinstance(obj, list):
        return obj

    return [obj]
