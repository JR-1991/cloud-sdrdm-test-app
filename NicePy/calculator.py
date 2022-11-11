class Calculator:
    """
    This is the same class as in the specs, but to demo how to
    pass data from the sdRDM interface to any arbitrary class or function.
    """

    def __init__(self, number, exponent):
        self.number = number
        self.exponent = exponent

    def calculate(self) -> float:
        return self.number**self.exponent
