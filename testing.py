def mbound(c, n, rem, length):
    new_rem = rem
    nwin = (length)//n
    new_rem = max(0, new_rem - c*nwin)
    x = min((length)%n, c)
    new_rem -= x
    minuspen = min((length)%n - x, c)
    minuspen = min(minuspen, new_rem)
    new_rem -= minuspen
    return min(n,length)*max(new_rem, 0)

ce = 1
ne = 3
r = 3
remaining = 2
print(mbound(ce, ne, r, remaining))