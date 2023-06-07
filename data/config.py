from dataclasses import dataclass


@dataclass
class Tokens:
    user: str = 'vk1.a.uzZ3YeokXabYndfSOhUoDGRDX2X0FH6w542lHi6_6IIFbxqQ20VIBx6MKUQaT6qof5tlSwnCcJKFSwK_PtCXW_iWW50eGgc7kKSbMnqzyZe1VZlN8GnJ15_rnPV5-MfV5t5ogfhY1812mePmjAPCXt2MvcUxeSH_OK-jlOM0yBsfs4d-knLWz_eJskPqnqODnzSDDXGUVLUrXezAb255VA'
    group: str = 'vk1.a.bhIF7gg1HFJQHy_mWOVTudihKtc0K0RYWUmgmcMtvWg2aVQIapjYulaCN7BvycYxRgHxIHyxvXEkCYx9zvQKI4zhjlTZhlJzN2ox0rWVefp3coatr_VdSLHO4ht4My6CZzAIfy2UaM0rafsll8CQSM8gCbG3j4VnLcyKKpajymnYdLsuczRLcWa-ZukQrfxPys8chhJbsUqs5pXiRgMNWg'


@dataclass
class Main:
    delta: int = 2
    offset: int = 0
    count: int = 50
