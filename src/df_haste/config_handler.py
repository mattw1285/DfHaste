## Standard Library Imports ##
from pathlib import Path
import tomllib
from typing import Self, Literal
from abc import ABC, abstractmethod

## Third Party Imports ##
from pydantic import BaseModel, model_validator


class BaseDbConfig(ABC, BaseModel):
    """ Pydantic and ABC validation on db connection config. 

    This is a base template to inherit from and should not be instantiated! The
    url method is defined as the clean ineterface to be called. Responsibilty 
    is given only to handle config read, all other 

    Attributes:
        name: unique string to identify an object
        driver: the name of the python driver
    """
    name: str
    driver: str

    @property
    @abstractmethod
    def url(self) -> str:
        """ Returns SqlAlchemy connection url.

        Universal interface to allow for creating connections, SQLAlchemy 
        is the driver for this. Children must implement to maintain the engine 
        creation interface.
        """
        pass 


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


class SQLServerConfig(BaseDbConfig):
    driver: Literal['pyodbc']
    
    def url(self) -> str: 
        return f'{driver}://'


class OracleDbConfig(BaseDbConfig):
    driver: Literal['cx_oracle', 'oracledb']
    port: int
    service_name: str|None
    sid: str|None
    username: str
    password: str

    def url(self) -> str: 
        return f'{driver}://'


DbConfig = (SQLiteConfig | OracleDbConfig | SQLServerConfig)
       

class SqlQuery(BaseModel):
    """ Pydantic BaseModel to cover saved queries metadata

    ## Write Me! ##
    """
    pass


class ConfigHandler:
    """ A class to abstract config file reads!

    Parent class to handle pydantic components.
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
        env = cls._read_config()
        env = env.get('ENVIRONMENT_CONFIG')
        if env is None:
            raise KeyError('ENVIRONMENT_CONFIG not defined!')
        with open(Path(env),'rb') as f:
            env = tomllib.load(f)
        return env


print(ConfigHandler.get_db('test'))
print(__file__)
