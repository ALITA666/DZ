from dataclasses import dataclass


@dataclass
class Tokens:
    user: str = '1'
    group: str = '2'


@dataclass
class Main:
    delta: int = 2
    offset: int = 0
    count: int = 50
