## Standard Library Imports ##
import tomllib
from pathlib import Path
from typing import Self, Literal

## Third Party Imports ##
from pydantic import (
    BaseModel,
    model_validator
)


class BaseDbConfig(BaseModel):
    name: str
    driver: str


class BasicAuthConfig(BaseDbConfig):
    driver: Literal['cx_oracle', 'oracledb']
    port: int
    service_name: str|None
    sid: str|None
    username: str
    password: str


class SQLiteConfig(BaseModel):
    name: str
    driver: Literal['sqlite3']
    path: Path

    @model_validator(mode='after')
    def validate_path(self) -> Self:
        if not self.path.exists ():
            raise ValueError(f"Invalid 'path' to {self.name} (sqlite3)")
        return self


class UnkownDbConfig(BaseDbConfig):
    hostname: str
    port: int
    service_name: str|None
    sid: str|None
    username: str
    password: str


DatabaseConfig = (
    SQLiteConfig
    | OracleDbConfig
    | UnkownDbConfig
)
_adapter = TypeAdapter(DatabaseConfig)
       

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
