
def is_prime(n: int) -> bool:
    """
    ============================================================================
     Check if a number is prime (brute-force primality test).
    ============================================================================
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def count_primes(nums: list[int]) -> int:
    """
    ============================================================================
     Count prime numbers in a list.
    ============================================================================
    """
    return sum(1 for n in nums if is_prime(n))
