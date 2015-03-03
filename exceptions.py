"""
Exceptions used by DummyData
"""

class DDException(Exception):
    """
    Base DummyData exception
    """
    pass


class DDEvaluatorException(DDException):
    """
    Exception thrown by DummyData evaluator
    """
    pass


class DDFunctionException(DDException):
    """
    Exception thrown by DummyData function
    """
    pass
