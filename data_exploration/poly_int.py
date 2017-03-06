import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('gyro_x.csv')

x = df['Time'].as_matrix()
y = df['X'].as_matrix()

plt.plot(x, y)
plt.show()

print(x)

print(y)
