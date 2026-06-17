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
    pss


class ConfigHandler:
    """ A class to abstract config file reads!

    Parent class to handle pydantic components.
    ## Write Me! ##
    """
    _default_path = Path('./df_haste.toml')

    @classmethod
    def _read_config(
        cls, 
        config_path:Path = _default_path
    ) -> dict:
        """ Returns a dict of """
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
        return data
 
    @classmethod
    def databases(cls) -> list[str]:
        """ Returns a list of availabe db connections. """
        pass
   
    @classmethod
    def get_db(cls, name:str) -> DbConfig:
        """ Getter method for DbConfig objects. """
        env = cls._read_config()
        env = env.get('ENVIRONMENT_CONFIG')
        if env is None:
            raise KeyError('ENVIRONMENT_CONFIG not defined!')
        with open(Path(env),'rb') as f:
            env = tomllib.load(f)
        return env

    @classmethod
    def sql_queries(cls) -> list[str]:
        pass

    @classmethod
    def sql_query(cls) -> SqlQuery:
        pass

if __name__ == '__main__':
    print(ConfigHandler.get_db(':memory:'))
