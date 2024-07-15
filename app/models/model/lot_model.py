from ..entity import Lot
from .base_model import Model

class LotModel(Model):
    def __init__(self):
        super().__init__("lots", Lot())