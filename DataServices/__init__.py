class Datum:
    """
    Returns Datum Object which is suitable for doing ...
    """

    def __init__(self, dict):
        """
        TODO: convert values to appropriate types.
        :param dict:
        """
        for i in dict:
            self.__dict__[i] = dict[i]
        pass

