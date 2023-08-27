import numpy as np
import matplotlib.pyplot as plt
import imageio

# Simülasyon için parametreler
num_frames = 100  # kare sayısı
circle_radius = 0.005  # Mekiği noktasal göster
y_min, y_max = 0, 1
circle_x = (y_max - y_min) / 2
plane_speed = (y_max - y_min - 2 * circle_radius) / (num_frames - 1)
wave_increment = plane_speed / 1.1  # Mach hızını değiştirmek için 1.1 değerini değiştir. Şu anda 1.1 Mach.
grid_size = 300

x = np.linspace(y_min, y_max, grid_size)
y = np.linspace(y_min, y_max, grid_size)
X, Y = np.meshgrid(x, y)

# Bu kısım dalgaları takip ediyor
waves = []

def gaussian2D(x, y, x0, y0, sx, sy, amplitude):
    return amplitude * np.exp(-((x - x0)**2 / (2 * sx**2) + (y - y0)**2 / (2 * sy**2)))

def update_circle_pos(frame):
    ax.clear()
    ax.set_xlim(y_min, y_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal', 'box')
    ax.axis('off')

    circle_y = y_min + frame * plane_speed

    # Yeni dalga yay
    waves.append([circle_x, circle_y, 0, 1.0])

    # Dalgalar için sıcaklık haritası
    heatmap = np.zeros_like(X)
    new_waves = []
    for wave in waves:
        wave[2] += wave_increment
        wave[3] *= 0.95
        heatmap += gaussian2D(X, Y, wave[0], wave[1], wave[2], wave[2], wave[3])
        if wave[2] + wave_increment < y_max - wave[1]:
            new_waves.append(wave)
    waves[:] = new_waves

    ax.imshow(heatmap, extent=(y_min, y_max, y_min, y_max), origin='lower', cmap='hot', aspect='auto', alpha=0.6)

    # Çiz
    plane_circle = plt.Circle((circle_x, circle_y), circle_radius, color='blue')
    ax.add_patch(plane_circle)
    return ax,

fig, ax = plt.subplots(figsize=(6, 6))

frames = []
for frame in range(num_frames):
    update_circle_pos(frame)
    fig.canvas.draw()  # Figürü update et
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    frames.append(image)

plt.close(fig)

# GIF olarak kaydet
imageio.mimsave('uzay_mekigi_simulasyon.gif', frames, duration=100)
