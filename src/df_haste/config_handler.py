## Standard Library Imports ##
from pathlib import Path
import tomllib
from typing import Self, Literal
from abc import ABC, abstractmethod

## Third Party Imports ##
from pydantic import BaseModel, model_validator


class BaseDbConfig(ABC, BaseModel):
    """ """
    name: str
    driver: str

    @property
    @abstractmethod
    def url(self) -> str:
        pass


class OracleDbConfig(BaseDbConfig):
    driver: Literal['cx_oracle', 'oracledb']
    port: int
    service_name: str|None
    sid: str|None
    username: str
    password: str

    def url(self) -> str: 
        return f'{driver}://'


class SQLiteConfig(BaseDbConfig):
    driver: Literal['sqlite3']
    path: Path

    @model_validator(mode='after')
    def validate_path(self) -> Self:
        if not self.path.exists ():
            raise ValueError(f"Invalid 'path' to {self.name} (sqlite3)")
        return self

    def url(self) -> str: 
        return f'oracle+{driver}://'


DbConfig = SQLiteConfig | OracleDbConfig 
       

class SqlQuery(BaseModel):
    """ Pydantic BaseModel to cover saved queries metadata

    ## Write Me! ##
    """
    pass


class ConfigHandler():
    """ Parent class to handle pydantic components.

    ## Write Me! ##
    """
    _default_path = Path(__file__).parent / 'config.toml'

    @classmethod
    def _read_config(
            cls, 
            config_path:Path = _default_path
    ) -> dict:
        """ ## Write Me! ## """
        config_path = Path(__file__).parent / 'config.toml'
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
        return data
 
    @classmethod
    def databases(cls) -> list[str]:
        """ Responsible for serving database config objects. """
        pass
    
    @classmethod
    def sql_queries(cls) -> list[SqlQuery]:
        pass

    @classmethod
    def get_db(cls, name:str) -> DbConfig:
        attrb = cls._read_config()
        return attrb

print(ConfigHandler.get_db('test'))
