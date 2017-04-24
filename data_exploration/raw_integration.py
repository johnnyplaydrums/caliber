import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import simps
from matplotlib.backends.backend_pdf import PdfPages

"""pp = PdfPages('multipage.pdf')
chunksize = 20
total_area = []
count = 0

for df in pd.read_csv('gyro_x.csv', chunksize=chunksize, iterator=True):

	x = df['Time'].as_matrix()
	y = df['X'].as_matrix()

	area = simps(y)
	print(area)
	print(count)
	total_area.append(abs(area))
	plt.plot(x, y)
	pp.savefig()
	plt.clf()
	count += 1


pp.close()
print(total_area)"""


def integrate(filename):
    chunksize = 20
    total_area = []

    for df in pd.read_csv('gyro_x.csv', chunksize=chunksize, iterator=True):

        x = df['X'].as_matrix()
        y = df['Y'].as_matrix()
        z = df['Z'].as_matrix()
        area_x = simps(x)
        area_y = simps(y)
        area_z = simps(z)
        area = area_x + area_y + area_z
        total_area.append(abs(area))

    return total_area

print(integrate('gyro_x.csv'))
