# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Material(Entity):
    id: int = 0
    lot_name: str  = ""
    name: str = ""
    into_account: int = 0
    in_good: int = 0
    in_store: int = 0
    be: int = 0
    breakdown: int = 0
    grade: str = ""
    full_name: str = ""
    contact: str = ""
    motif: str = ""
    place: str = ""
    date_perc: str = ""
    date_reinteg: str = ""
    state_mat_integr: str = ""