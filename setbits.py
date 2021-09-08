# -*- coding: utf-8 -*-
def setbits(number):
    try:
        n=float(number)
        n="{:.5e}".format(n)
        if float(n[-3:]) <= -5 or float(n[-3:]) >= 5:
            return n
        else:
            return str(round(float(n), 5))
            #return "{:.4f}".format(float(number))
    except:
        return number
