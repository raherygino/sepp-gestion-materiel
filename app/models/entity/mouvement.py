# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Mouvement(Entity):
    id: int = 0
    material_id: int  = 0
    in_good: int = 0
    grade: str = ""
    full_name: str = ""
    contact: str = ""
    motif: str = ""
    place: str = ""
    be: int = 0
    breakdown: int = 0
    date_perc: str = ""
    date_reinteg: str = ""
    state_mat_integr: str = ""