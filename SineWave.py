import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 12 * np.pi, 1000)
plt.plot(x, np.sin(x))
plt.xlabel("Angle [rad]")
plt.ylabel("sin(x)")
plt.axis('tight')
plt.savefig("result/sinewave.png")