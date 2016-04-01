# vedic-py
Python library for Vedic Maths sutras. This library implements the vedic
maths sutras for performing basic mathematical operations like addition, subtraction, multiplication,
square roots, cube roots etc.

The library will also expose operations like factorial. This library can be used to
perform very large multiplications. Though python does not have any restrictions
on size of integers, floats many programming languages do.

Since vedic maths sutras work on individual digits in a number as opposed to the
whole number, they can treat numbers as strings and hence not run into issues with storage
and computations on very large numbers.

## Representation
The python library exposes a construct called **VedicNumber** which is an abstraction over
basic constructs (integers, strings etc.)

```python
from vedic import VedicNumber

myintvedicnumber = VedicNumber(100)
mystrvedicnumber = VedicNumber('1897656578')
```

## Addition
Two vedic numbers can be added using the **+** operator as follows. Addition
is performed using the L-R vedic sutra.

```python
from vedic import VedicNumber

vedicnumber1 = VedicNumber(1234)
vedicnumber2 = VedicNumber(5678)

result = vedicnumber1 + vedicnumber2
print(result)
```

For adding multiple numbers at a time, the API can be used as follows

```python
from vedic import Ops, VedicNumber

result = Ops.add([58200, 1136909 + 14567 + 345687000, 45678])
# Vedic numbers can be passed to the above add api as well
print(result)
```

## Subtraction
A vedic number can be subtracted from another vedic number. This uses the L-R vedic sutra.

```python
from vedic import VedicNumber

result = VedicNumber(90008988) - VedicNumber(28200009)
print(result)

result = VedicNumber(100020000000000) - VedicNumber(9)
print(result)
```

## Multiplication
Two vedic numbers can be multiplied using the * operator of python. The multiplication
is performed using Vertical-Crosswise sutra of vedic maths

```python
from vedic import VedicNumber

print(VedicNumber(45) * VedicNumber(57))

#Really large numbers
print(VedicNumber(68629335010652649695338856996888505082799258781159071602280830658069423538482865002531059244901433270522974099404725678) * VedicNumber(4681792376906432202903607601716785597020499902587316420748476976419066198975454254254254278899))
```


**P.S** - THIS LIBRARY IS STILL WIP

