import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x = np.linspace(0, 2 * np.pi, 500)

fig, ax = plt.subplots(figsize=(10, 5))
line_sin, = ax.plot(x, np.sin(x), label='sin(x)', color='blue')
line_cos, = ax.plot(x, np.cos(x), label='cos(x)', color='red')
ax.set_title('Sine and Cosine Waves')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.grid(True)
ax.set_ylim(-1.5, 1.5)

def animate(frame):
    phase = frame * 0.05
    line_sin.set_ydata(np.sin(x + phase))
    line_cos.set_ydata(np.cos(x + phase))
    return line_sin, line_cos

ani = FuncAnimation(fig, animate, interval=50, blit=True, cache_frame_data=False)
plt.show()
