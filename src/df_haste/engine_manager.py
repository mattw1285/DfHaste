## Standard Library Imports ##
import json
import os

## Third-party Library Imports ##
from sqlalchemy import (
    create_engine,
    Engine
)

## Local Library Imports ##
from .config_handler import ConfigHandler


class engine_manager:
    """ Central factory and register for SQLAlchemy Engine instances.
    
    Prevents redundant connection pools by caching engines. Designed to be 
    initialized once per db and simplify initialisation.
    """
    def __init__(
        self, 
        config_path: str = os.path.join(
            os.path.dirname(__file__),
            'config.json'
        )
    ):
        self._engines = {}
        with open(config_path, 'r') as config_file:
            self._db_config = json.load(config_file)
        self._db_config = self._db_config['db_connections']
        
    def get_engine(self, db_name: str) -> Engine:
        """    Get method to return a db Engine

        Checks central register and creates if missing.
        """
        db_engine = self._engines.get(db_name)
        if db_engine is None:
            conn_string = self._db_config[db_name]['conn_string']
            db_engine = create_engine(conn_string)
            self._engines[db_name] = db_engine
      return db_engine
