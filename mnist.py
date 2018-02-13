import struct
from itertools import izip
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

def read_dataset(imagefile_path="", labelfile_path=""):
    labels = read_label_file(labelfile_path)
    images = read_image_file(imagefile_path)

    for image, label in izip(images, labels):
        yield {'image':image, 'label':label}


def read_label_file(labelfile_path):
    with open(labelfile_path, 'rb') as labelfile:

        # Read the file header
        magic_number = struct.unpack('>i', labelfile.read(4))[0]
        num_items = struct.unpack('>i', labelfile.read(4))[0]

        # Check the magic number
        if not magic_number == 2049:
            print("Error: something went wrong while reading the header of " + labelfile_path)
            exit(1)

        # Extract labels
        try:
            label = labelfile.read(1)
            while(label != b""):
                yield struct.unpack('>B', label)[0]
                label = labelfile.read(1)
        finally:
            pass


def read_image_file(imagefile_path):
    with open(imagefile_path, 'rb') as imagefile:

        # Read the file header
        magic_number = struct.unpack('>i', imagefile.read(4))[0]
        num_items = struct.unpack('>i', imagefile.read(4))[0]
        num_rows = struct.unpack('>i', imagefile.read(4))[0]
        num_cols = struct.unpack('>i', imagefile.read(4))[0]

        image_size = num_rows * num_cols

        # Chech the magic number
        if not magic_number == 2051:
            print("Error: something went wrong while reading the header of " + imagefile_path)
            exit(1)

        # Extract images
        try:
            image = imagefile.read(image_size)
            while(image):
                image_arr = list([struct.unpack('>B', x)[0] for x in image])

                yield image_arr

                image = imagefile.read(image_size)

        finally:
            imagefile.close()


def image2arr_2d(image):
    image_arr_2d = []

    for row in range(28):
        row_offset = 28 * row
        image_arr_2d.append(list(x for x in image[row_offset:(row_offset + 28)]))

    return image_arr_2d


def plot_image(image):
    I = np.array(image2arr_2d(image))

    plt.imshow(I)
    plt.show()


if __name__ == "__main__":
    datasets = {}
    datasets['test'] = read_dataset(labelfile_path="mnist_data/t10k-labels-idx1-ubyte",
                                     imagefile_path="mnist_data/t10k-images-idx3-ubyte")

    datasets['train'] = read_dataset(labelfile_path="mnist_data/train-labels-idx1-ubyte",
                                    imagefile_path="mnist_data/train-images-idx3-ubyte")

    print("Displaying a few images")

    num_of_images_to_show = 5
    for item in datasets['train']:
        if num_of_images_to_show == 0:
            break

        plot_image(item['image'])

        num_of_images_to_show -= 1
