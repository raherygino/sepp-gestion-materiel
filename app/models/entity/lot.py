# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Lot(Entity):
    id: int = 0
    name: str = ""