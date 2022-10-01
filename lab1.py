import matplotlib.pyplot as pyplot
import control.matlab as matlab
import colorama as color


# Link selection method
def choise():
    inertialessUnitName = "Inertia - free link"
    aperiodicUnitName = "Aperiodic link"
    realdifferUnitName = "The real differentiating link"
    integratingUnitName = "Integrating link"
    idealdifferUnitName = "The ideal differentiating link"

    needNewChoise = True

    # Entering commands in the terminal
    while needNewChoise:
        print(color.Style.RESET_ALL)
        userInput = input("Enter the command number: \n"
                          "1 - " + inertialessUnitName + ";\n"
                                                         "2 - " + aperiodicUnitName + ";\n"
                                                                                      "3 - " + realdifferUnitName + ";\n"
                                                                                                                    "4 - " + idealdifferUnitName + ";\n"
                                                                                                                                                   "5 - " + integratingUnitName + ".\n")

        if userInput.isdigit():
            needNewChoise = False
            userInput = int(userInput)
            if userInput == 1:
                name = "Inertia - free link"
            elif userInput == 2:
                name = "Aperiodic link"
            elif userInput == 3:
                name = "The real differentiating link"
            elif userInput == 4:
                name = "The ideal differentiating link"
            elif userInput == 5:
                name = "Integrating link"

            else:
                print(color.Fore.RED + "\nInvalid value!")
                needNewChoise = True


        else:
            print(color.Fore.RED + "\nPlease enter a numeric value!")
            needNewChoise = True
    return name


# Mathematical description of a link by its name
def getUnit(name):
    needNewChoise = True
    while needNewChoise:
        print(color.Style.RESET_ALL)
        needNewChoise = False
        k = input('please enter the coefficient "k": ')
        t = input('please enter the coefficient "t": ')

        if k.isdigit() and t.isdigit():
            k = int(k)
            t = int(t)
            if name == "Inertia - free link":
                unit = matlab.tf([k], [1])
            elif name == "Aperiodic link":
                unit = matlab.tf([k], [t, 1])
            elif name == "The real differentiating link":
                unit = matlab.tf([k, 0], [t, 1])
            elif name == "The ideal differentiating link":
                unit = matlab.tf([k, 0], [1 / 1000, 1])
            elif name == "Integrating link":
                unit = matlab.tf([1], [t, 0])

        else:
            print(color.Fore.RED + "\nPlease enter a numeric value!")
            needNewChoise = True
    return unit


# Plotting
def graph(num, title, y, x):
    pyplot.subplot(2, 1, num)
    pyplot.grid(True)
    if title == "Transitional characteristic":
        pyplot.plot(x, y, "purple")
    elif title == "Impulse response":
        pyplot.plot(x, y, "green")

    pyplot.title(title)
    pyplot.ylabel("Amplitude")
    pyplot.xlabel("Time (sec)")


unitName = choise()
unit = getUnit(unitName)

timeLine = []
for i in range(0, 10000):
    timeLine.append(i / 1000)

[y, x] = matlab.step(unit, timeLine)
graph(1, "Transitional characteristic", y, x)
[y, x] = matlab.impulse(unit, timeLine)
graph(2, "Impulse response", y, x)

# АЧХ and ФЧХ
pyplot.show()
matlab.bode(unit, dB=False)
pyplot.plot()
pyplot.xlabel("Frequency, Hz")
pyplot.show()
