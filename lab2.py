import control
import matplotlib.pyplot
import sympy as sympy
import numpy as numpy
import matplotlib.pyplot as plt
import control.matlab as mtb

Koc = 8
# Initial data
OS = mtb.tf([Koc, 0], [0, 1])
GEN = mtb.tf([1], [7, 1])
GTurb = mtb.tf([0.02, 1], [0.35, 1])
IUstr = mtb.tf([24], [5, 1])
W = GEN * GTurb * IUstr
Wzam = mtb.feedback(W, OS)
Wraz = W

print("W(p) of a closed system")
print(Wzam)

# Function for constructing a transition characteristic
[y, x] = mtb.step(Wzam)
plt.plot(x, y)
plt.title("h(t)")
plt.xlabel("time (c)")
plt.ylabel("amplitude")
plt.grid(True)
plt.show()


# Determination of poles W(p) of a closed ACS
a = mtb.pole(Wzam)
b = mtb.zero(Wzam)
print("Poles W(p) of a closed ACS:\n", a)
print("Zeros W(p) of a closed ACS:\n", b)
stab = True

control.pzmap(Wzam, title="Map of poles and zeros Wzam")
plt.show()

print("W(p) of an open system")
print(Wraz)

for i in mtb.pole(Wzam):
    if i.real > 0:
        stab = False

print("stable" if stab else "unstable")

# Function for constructing a Nyquist Hodograph
mtb.nyquist(Wraz)
plt.grid(True)
plt.title("Nyquist 's Hodograph")
plt.xlabel("Re")
plt.ylabel("Im")
plt.show()

# Function for constructing ЛАЧХ and ЛФЧХ
mtb.bode(Wraz, omega_limits=[0.01, 1e3])
plt.show()

def fCh():
    print("ЛАЧХ and ЛФЧХ shown on the graph.\n")
    mtb.bode(Wraz, dB=False)
    plt.plot()
    plt.xlabel("Frequency (Hz)")
    plt.show()

# Mikhailov
# Summing up the numerator and denominator Wzam
sumnum = [float(x) for x in Wzam.num[0][0]]
sumden = [float(x) for x in Wzam.den[0][0]]
funmikh = []
print(funmikh)
for i in range(len(sumden) - len(sumnum)):
    sumnum.insert(0, 0)
for i in range(len(sumnum)):
    funmikh.append(sumnum[i] + sumden[i])
print(funmikh)
# stability
funmikh = funmikh[::-1]
j = sympy.I
om = sympy.symbols("w")
for i in range(len(funmikh)):
    funmikh[i] = funmikh[i] * (j * om) ** i
x = numpy.arange(0, 20, 0.01)
mc = []
for i in x:
    sum = 0
    for k in funmikh:
        sum += k.subs(om, i)
    mc.append(sum)

real = [sympy.re(x) for x in mc]
imaginary = [sympy.im(x) for x in mc]
num = 1
flagcros = False
flagposcrosX = True
flagposcrosY = True
for i in range(len(mc) - 1):
    if ((real[i] >= 0 and real[i + 1] <= 0) or (real[i] <= 0 and real[i + 1] >= 0)):
        if flagposcrosX:
            num += 1
            flagposcrosX = False
            flagposcrosX = True
        if imaginary[i] > 0:
            flagcros = True
    if ((imaginary[i] >= 0 and imaginary[i + 1] <= 0) or (imaginary[i] <= 0 and imaginary[i + 1] >= 0)):
        if flagposcrosY:
            num += 1
            flagposcrosX = True
            flagposcrosX = False
    if num >= 3 and flagcros:
        print("The system is unstable")
    else:
        print("The system is stable")
        break

plt.title("Mikhailov")
ex = matplotlib.pyplot.gca()
ex.plot(real, imaginary)
ex.grid(True)
ex.spines["left"].set_position("zero")
ex.spines["right"].set_color("none")
ex.spines["bottom"].set_position("zero")
ex.spines["top"].set_color("none")
plt.xlim(-1000, 1000)
plt.ylim(-1000, 1000)
plt.xlabel("re")
plt.ylabel("im")
plt.show()

# Search for Koc
for Koc in numpy.arange(0, 100, 0.01):
    OS = mtb.tf([Koc, 0], [0, 1])
    Wzam = mtb.feedback(W, OS)
    c = Wzam.den[0][0]
    cf = {}
    size = len(c)
    for j in range(0, size):
        cf["%s" % j] = c[j]
    matrix = numpy.array([[cf["1"], cf["3"]], [cf["0"], cf["2"]]])
    if (numpy.linalg.det(matrix) >= -0.0001) & (numpy.linalg.det(matrix) <= 0.0001):
        print("Limit value Koc:", Koc)
        break
