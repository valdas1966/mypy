import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)

# fake up some data
spread = [1,2,3,3,3,4,5]
center = [1,1,1,1,1,1,1]
flier_high = [5,5,5,5,5,5,5]
flier_low = [1,1,1,1,1,1,1]
data = np.concatenate((spread, center, flier_high, flier_low))
data = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,3,3,3,4,5]

fig1, ax1 = plt.subplots()
ax1.set_title('Basic Plot')
ax1.boxplot(data)