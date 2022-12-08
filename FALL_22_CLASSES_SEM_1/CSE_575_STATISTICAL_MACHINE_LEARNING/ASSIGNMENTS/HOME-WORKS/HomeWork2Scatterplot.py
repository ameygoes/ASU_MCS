# ======================================================
# Copyright (c) Amey Bhilegaonkar. All rights reserved.
# AUTHOR: AMEY BHILEGAONKAR
# PORTFOLIO: https://ameyportfolio.netlify.app
# ======================================================

import matplotlib.pyplot as plt

# Data(−3,2.5)
x1 = [-2, 0, -3]
y1 = [0,2, 2.5]
x2 = [2,2,3]
y2 = [2,0,-1]

# Plot
plt.scatter(x1,y1,color='blue')
plt.scatter(x2,y2,color= 'red')
plt.axvline(1, color='r', linestyle='-')
plt.rcParams.update({'figure.figsize':(10,8), 'figure.dpi':10000})

# Decorate
plt.title('Color Change')
plt.xlabel('X - value')
plt.ylabel('Y - value')
plt.show()