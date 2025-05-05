
class UInterpolation:
    """
    ===========================================================================
     Utils-Class for Number-Interpolation.   
     Supports linear interpolation for scalars and sequences. 
    ===========================================================================
    """

    @staticmethod
    def linear(# Start-Value
               a: float,
               # Finish-Value
               b: float,
               # Factor (between 0 and 1)
               t: float) -> float:
        """
        ===========================================================================
         Linear-Interpolation between two numbers.
         Returns a number between A and B, based on a given factor t ∈ [0, 1].
         For example, the factor t=0.5 is the midpoint between A and B.
        ===========================================================================
         Use Cases:
        ---------------------------------------------------------------------------
            1. Scaling values between known bounds.
            2. Generating color gradients (ex: light to dark)
        ===========================================================================
         Example: liner(a=2, b=4, t=0.5) -> 3.0
        ===========================================================================
        """
        # Calculate the distance between the two numbers.
        distance = b - a
        # Calculate the interpolated addition.
        addition = distance * t
        # Return the interpolated value.
        return a + addition

    @staticmethod
    def linear_list(# Start-Value
                    a: float,
                    # Finish-Value
                    b: float,
                    # Number of steps
                    n: int) -> list[float]:
        """
        ===========================================================================
         Returns a list of n-floats, linearly interpolated between A and B.
        ===========================================================================
         When to use:
        ---------------------------------------------------------------------------
            1. When you need a linear list of values between two numbers.
               Ex: [2, 2.5, 3, 3.5, 4]            
            2. When you need to create a gradient between two numbers.
               Ex: [Light-Gray, Gray, Dark-Gray]
        ===========================================================================
         Example: linear_list(a=2, b=4, n=3) -> [2, 3, 4]
        ===========================================================================
        """
        # Initialize the result list.
        res: list[float] = list()
        # Calculate the step size.
        step = (b - a) / (n - 1)
        # Calculate the list of values.
        for i in range(n):
            # Calculate the addition to A for each step.
            addition = i * step
            # Append the interpolated value to the result list.
            res.append(a + addition)
        # Return the result list.
        return res
        # return np.linspace(start=a, stop=b, num=n)