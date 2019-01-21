# -*- coding: utf-8 -*-
#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import cv2

x = np.arange(0, 5, 0.1)
print x
y = np.sin(x)
print y
plt.plot(x, y)