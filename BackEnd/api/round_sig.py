# used to round values to n-significant figues

from math import log10, floor

def round_sig(x, sig=2):
    if x == 0:
        return 0

    return round(x, sig-int(floor(log10(abs(x))))-1)