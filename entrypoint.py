from NicePy.calculator import Calculator

def main(model):
    """This function executes the process this thin layer has been built for :-)"""
    
    # Pass the data from the sdRDM model to
    # the application
    calculator = Calculator(
        number=model.number,
        exponent=model.exponent
    )
    
    # Do some fancy calculations
    result = calculator.calculate()
    
    # Write the result back into the application
    # model where an explicit result section is given
    model.add_to_results(number=result)
    
    return model
    