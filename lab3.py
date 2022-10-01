import colorama
import control as ctl
import numpy
import matplotlib.pyplot as plt
import sympy
import control.matlab as mtb
import math
from scipy import integrate


def reg(sau):
    if sau == "PID":
        kp = 0.2998
        ki = 0.0348
        kd = 0.3997
        p = mtb.tf([kp], [1])
        i = mtb.tf([ki], [1, 0])
        d = mtb.tf([kd, 0], [1])
        pid = ctl.parallel(p, i, d)
        return pid
    elif sau == 'PI':
        kp = 0.247
        ki = 0.01
        p = mtb.tf([kp], [1])
        i = mtb.tf([ki], [1, 0])
        pi = ctl.parallel(p, i)
        return pi


sau_reg = input("Enter the name of the controller (PID or PI):")
# Transfer functions of structural diagram links
OS = mtb.tf([1], [1])
GEN = mtb.tf([1], [7, 1])
print("Wg = ", GEN)
GTurb = mtb.tf([0.02, 1], [0.35, 1])
print("Wgt = ", GTurb)
IUstr = mtb.tf([24], [5, 1])
print("Wiu = ", IUstr)

# Transformation of the block diagram
W = ctl.series(reg(sau_reg), GEN, GTurb, IUstr)
print(W)
Wzam = mtb.feedback(W, OS)
print(Wzam)

# 3. Direct quality assessments of PP
# Transitional characteristic
timeLine = numpy.arange(0, 100, 0.1)
plt.subplot(1, 1, 1)
plt.grid(True)
y, x = mtb.step(Wzam, timeLine)
# Removing the maximum
ind1 = numpy.argmax(y)
index1 = []
for i in range(0, ind1):
    index1.append(i)
y1 = numpy.delete(y, index1)
x1 = numpy.delete(x, index1)
# The first maximum
max1 = max(y)  # value
t1max3 = None
for i in range(len(y) - 1):
    if y[i] == max1:
        t1max3 = x[i]  # time
t_infinity = 100
t = None
# Finding the steady-state value
for i in range(len(x1) - 1):
    if x1[i] <= t_infinity:
        t = i
h_infinity = y1[t]
h_yst1 = h_infinity * 1.03
h_yst2 = h_infinity * 0.97
# Finding the time of the steady value
treg3 = None
reg_i = None
for i in range(t):
    if (h_yst1 - 0.001 < y1[i] < h_yst1 + 0.001) or (h_yst2 - 0.001 < y1[i] < h_yst2 + 0.001):
        treg3 = x1[i]
# Degree of attenuation
# Finding the minimum after the first maximum
ind2 = numpy.argmin(y1)
index2 = []
for i in range(0, ind1):
    index2.append(i)
y2 = numpy.delete(y1, index2)
x2 = numpy.delete(x1, index2)
# Finding the second maximum
max2 = max(y2)
zat3 = (max1 - max2) / max1
coleb3 = max1 / max2
per3 = ((max1 - h_infinity) / h_infinity) * 100
# Let's display the values of 3
print(colorama.Fore.BLUE)
print("3. Direct quality assessments of PP")
print("a) Regulation time:", treg3)
print("b) Over-regulation:", per3)
print("c) Oscillation:", coleb3)
print("d) Degree of attenuation:", zat3)
print("e) The value of reaching the first maximum:", max1)
print("Time to reach the first maximum:", t1max3)
plt.plot(x, y, "red")
plt.title("Transitional characteristic")
plt.ylabel("Amplitude")
plt.xlabel("time, (с)")
plt.hlines(1.03 * y[len(timeLine) - 1], 0, 100)
plt.hlines(0.97 * y[len(timeLine) - 1], 0, 100)
plt.show()

# 4. By the distribution of roots on the complex plane Wzam
# Determining the value of the poles of the transfer function Wzam
a = mtb.pole(Wzam)
a = numpy.round(a, 3)
print("Полюса ПП Wzam:")
print(a)
mean = -1000
for i in range(len(a) - 2):
    if a[i].real >= mean:
        mean = a[i].real
treg4 = math.fabs(3 / mean)
# Determination of the maximum degree of oscillation
max4 = 0
coleb4 = 0
for i in a:
    coleb4 = math.fabs(sympy.im(i) / sympy.re(i))
    if coleb4 > max4:
        max4 = coleb4
coleb4 = max4
per4 = math.e ** (-math.pi / coleb4)
zat4 = 1 - math.e ** (-2 * math.pi / coleb4)
# Map of poles and zeros
ctl.pzmap(Wzam, title="Map of poles and zeros Wzam")
plt.show()
# Let's display the values of 4
print(colorama.Fore.CYAN)
print("4. By the distribution of roots on the complex plane Wzam")
print("a) Regulation time:", treg4)
print("b) Over-regulation:", per4)
print("c) Oscillation:", coleb4)
print("d) Degree of attenuation:", zat4)

# 5. ЛЧХ; Finding the oscillation index:
timeLine = numpy.arange(0, 5, 0.1)
plt.subplot(1, 1, 1)
plt.grid(True)
mag, phase, omega = mtb.freqresp(Wzam, timeLine)
logmax = max(mag)
log = mag[0]
ind_mag_max = numpy.argmax(mag)
# Removing values to the maximum
index_mag = []
for i in range(0, ind_mag_max):
    index_mag.append(i)
mag1 = numpy.delete(mag, index_mag)
omega1 = numpy.delete(omega, index_mag)
idfreqs = 0
for i in range(len(mag1) - 1):
    if mag1[i] >= mag[0] >= mag1[i + 1]:
        idfreqs = i
freqs = omega1[idfreqs]
treg5 = 1 * ((2 * math.pi) / freqs)
plt.plot(omega, mag, "red")
plt.title("АЧХ")
plt.ylabel("Amplitude")
plt.xlabel("Angular frequency, (рад/с)")
plt.hlines(mag[0], 0, 3, linestyles="--")
plt.show()
koleb5 = logmax / log
y = phase[i]
fase = 180 - abs(y)
print("Phase stability margin = ", fase)
k = 0
for i in range(len(phase)):
    if phase[i] == 180:
        k = 1
        idfreqs = i
        break
if k == 1:
    amp = abs(0 - mag[idfreqs])
else:
    amp = abs(0 - mag[-1])
print("Amplitude stability margin = ", amp)
print(colorama.Fore.RED)
print("The margin of stability in amplitude is equal to infinity, because the phase characteristic does not cross the line -180 degrees.")

# Let's display the values of 5
print(colorama.Fore.YELLOW)
print("5. ЛЧХ")
print("a) Regulation time:", treg5)
print("b) The oscillation index:", koleb5)
mag, phase, omega = mtb.bode(Wzam)
plt.show()

# Integral method:
timeLine = numpy.arange(0, 100, 0.1)
y, x = mtb.step(Wzam, timeLine)
integ = []
for i in y:
    integ.append(math.fabs(h_infinity - i))
Q = integrate.trapezoid(integ, x)
print(colorama.Fore.BLACK)
print("Integral method Q")
print("The value of the integral", Q)
print()
print("Quality indicators:")
print("Regulation time: 11 = ", treg3)
print("Over-regulation: 28 = ", per3)
print("The oscillation index: 1.23 = ", koleb5)
