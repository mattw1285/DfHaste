from sqlalchemy import create_engine

class EngineManager:
    """ A thin wrap on sqlalcehmy!

    The aim is to make working in an env with lots of db connections much more convenient
    """
    def __init__(self, config='sample_location'):
        self._engines = {}

    def get_engine(''):
        pass

    def dispose():
        pass

