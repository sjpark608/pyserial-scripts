import numpy as np
import matplotlib.pyplot as plt

# Generate random data for partial discharge events
row_size = 128
colum_size = 128
max_px = 255


def create_column(multiplier):
    column = np.concatenate((np.random.uniform(180,256,30).astype(int),
                             (np.random.uniform(1,2,45)).astype(int),
                             (np.random.uniform(800,900,5)*multiplier).astype(int),
                             (np.random.uniform(1,2,48)).astype(int)))
    # print(column)
    return column

def create_raster():
    image = []
    for indx in range(colum_size):
        image.append(create_column(0.1 if indx < 80 and indx>70 else 0))
    # image = np.transpose(np.array(image))
    image =np.array(image)
    # image =np.rot90(image, k=1)
    print(np.array(image))
    np.savetxt("rast_file", image, fmt='%d', delimiter=',')
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)
    plt.colorbar()
    plt.grid(visible=True, linestyle='--', linewidth=0.5)
    plt.show()


if __name__ == '__main__':
    create_raster()