import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import simps
from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('multipage.pdf')
chunksize = 20
total_area = []
count = 0

for df in pd.read_csv('gyro_x.csv', chunksize=chunksize, iterator=True):
	
	x = df['Time'].as_matrix()
	y = df['X'].as_matrix()

	area = simps(y)
	total_area.append(abs(area))
	plt.plot(x, y)
	pp.savefig()
	plt.clf()
	count += 1


pp.close()
print(total_area)
