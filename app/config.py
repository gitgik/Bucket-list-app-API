class BaseConfig(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """ Set debugging to true during dev """
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """ set testing to true during testing """
    DEBUG = False
    TESTING = True