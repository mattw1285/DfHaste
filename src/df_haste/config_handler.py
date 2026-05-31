## Standard Library Imports ##
import tomllib
from pathlib import Path
from typing import Self

## Third Party Imports ##
from pydantic import (
    BaseModel,
    model_validator
)

class DatabaseConfig(BaseModel):
    """ Pydantic BaseModel to encapsulate connection details 

    ## Write Me! ##
    """
    name: str
    driver: str
    hostname: str|None = None
    sid: str|None = None
    service_name: str|None = None
    path: Path|None = None
    username: str|None = None
    password: str|None = None

    @model_validator(mode='after')
    def validate_path(self) -> Self:
        if self.driver == 'sqlite3' and self.path is None:
            raise ValueError(f"{self.name} (sqlite3) needs a 'path'")
        elif self.driver != 'sqlite3' and self.path is not None:
            raise ValueError(f"only (sqlite3) needs a 'path' not {self.name}")
        return self

    @model_validator(mode='after')
    def validate_host(self) -> Self:
        pass

    @model_validator(mode='after')
    def validate_auth(self) -> Self:
        pass

       
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
    def databases(cls) -> list[DatabaseConfig]:
        """ Responsible for serving database config objects. """
        pass
    
    @classmethod
    def sql_queries(cls) -> list[SqlQuery]:
        pass

    @classmethod
    def get_database(self, name:str) -> DatabaseConfig:
        pass

print(ConfigHandler._read_config())
