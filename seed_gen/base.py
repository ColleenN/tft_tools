from abc import abstractmethod, ABCMeta
from csv import DictWriter
from pathlib import Path
from data_io.tft import TFTSetBlob


class SeedRegistry(ABCMeta, type):

    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        # instantiate a new type corresponding to the type of class being defined
        # this is currently RegisterBase but in child classes will be the child class
        new_cls = type.__new__(cls, name, bases, attrs)
        seed_name = getattr(new_cls, "seed_name")
        if seed_name:
            cls.REGISTRY[seed_name] = new_cls
        return new_cls

    @classmethod
    def get_registered_seeds(cls):
        return dict(cls.REGISTRY)


class TFTDataSeed(metaclass=SeedRegistry):

    seed_name = ""

    def __init__(self, set_blob=None, set_num=None):

        if set_blob:
            if set_num:
                raise ValueError("Cannot have both set_num and set_blob")
            self.set_blob = set_blob
        else:
            self.set_blob = TFTSetBlob(set_num=set_num)
        self._prepped_data = []

    def write_seed_data(self):

        with Path(f"seed_{self.seed_name}.csv").open('w', newline='') as csvfile:
            fieldnames = self.data[0].keys()
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)

    @property
    def data(self):
        if not self._prepped_data:
            self._prepped_data = self._prep_data()
        return self._prepped_data

    def _prep_data(self):
        raw_data_entries = self._extract()
        return [self._convert(x) for x in raw_data_entries if self._filter(x)]

    def _extract(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _filter(raw_record):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _convert(raw_record):
        raise NotImplementedError


def camel_to_snake(some_str):

    new_str = ""
    for char in some_str:
        if char.isupper():
            new_str += "_" + char.lower()
        else:
            new_str += char
    return new_str
