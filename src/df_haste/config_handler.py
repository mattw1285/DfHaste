## Standard Library Imports ##
import tomllib
from pathlib import Path

## Third Party Imports ##
from pydantic import BaseModel

class DatabaseConfig(BaseModel):
    """ Pydantic BaseModel to encapsulate connection details 

    ## Write Me! ##
    """
    name: str
    driver: str
    
class SqlQuery(BaseModel):
    path: Path

class ConfigHandler():
    """ Parent class to handle pydantic components.

    ## Write Me! ##
    """
    def __init__(self):
        with open('config.toml', "rb") as f:
            data = tomllib.load(f)
        data = data['database']
        d = {}
        for x in data:
            if x['name'] in d: 
                raise ValueError
            d[x['name']] = x 
            del d[x['name']]['name']
        print(d)

    def databases(self) -> list[DatabaseConfig]:
        """ Responsible for serving database config objects. """
        pass
    
    def sql_queries()
        pass
    
    
