from ..n2_module import func3

# from ..n2_module import func3
# from package.n2.n2_module import func3


def func4(param1: str, param2: dict):
    func3(param1, param2)
    return param1, param2


async def cofunc4():
    return 'ok'


class Class4:
    def __init__(self) -> None:
        pass

    def method4(self):
        return 'classic response'
