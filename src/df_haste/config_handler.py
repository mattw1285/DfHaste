## Standard Library Imports ##
from pathlib import Path
import tomllib
from typing import Self, Literal
from abc import ABC, abstractmethod

## Third Party Imports ##
from pydantic import BaseModel, model_validator


class BaseDbConfig(ABC, BaseModel):
    """ Pydantic and ABC base template for db connection configs. 

    Attributes:
        name: unique string to identify an object
        driver: the name of the python driver
        url(property): sqlalchemy connection url
    """
    name: str
    driver: str

    @property
    @abstractmethod
    def url(self) -> str:
        """ Returns SqlAlchemy connection url. """
        pass 


class SQLiteConfig(BaseDbConfig):
    """ A SQLite sepcific DbConfig implementation of BaseDbConfig.

    Attributes:
        path: file location or the ':memory:' edge case
    """
    driver: Literal['sqlite3']
    path: Path | Literal[':memory:']

    @model_validator(mode='after')
    def validate_path(self) -> Self:
        """ Validates the db path. """
        if self.path == ':memory:':
            return self
        if not self.path.exists ():
            raise ValueError(f"Invalid 'path' to {self.name} (sqlite3)")
        return self

    @property
    def url(self) -> str:
        """ Returns sqlalchemy sqlite engine connection url. """
        return f'sqlite:///{self.path}'


class SQLServerConfig(BaseDbConfig):
    """ An MS SQL Server specific DbConfig implementation of BaseDbConfig. """
    pass


class OracleDbConfig(BaseDbConfig):
    """ An Oracle specific DbConfig implementation of BaseDbConfig. """
    pass


class PgConfig(BaseDbConfig):
    """ A postgres specific DbConfig implementation of BaseDbConfig. """
    pass


DbConfig = (SQLiteConfig | OracleDbConfig | SQLServerConfig | PgConfig)
       

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
    def __init__(self, config_path: Path):
        if not config_path.exists():
            raise ValueError('Config file cannot be found!')
        self.config_path = config_path

    @property
    def _config(self) -> dict:
        """ Returns a dict of config. """
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
        return data

    @property
    def _env(self) -> dict:
        """ Returns a dict of env variables. """
        pass

    def databases(self) -> list[str]:
        """ Returns a list of availabe db connections. """
        pass
   
    def get_db(self, name:str) -> DbConfig:
        """ Getter method for DbConfig objects. """
        env = cls._read_config(config_path)
        env = env.get('ENVIRONMENT_CONFIG')
        if env is None:
            raise KeyError('ENVIRONMENT_CONFIG not defined!')
        return env

    def sql_queries(self) -> list[str]:
        pass

    def sql_query(self) -> SqlQuery:
        pass


if __name__ == '__main__':
    print(ConfigHandler.get_db(':memory:'))
