import SimpleITK as sitk
from matplotlib import pyplot as plt

# A Nii 3D data viewer
# Through this example,you can view any pieces of a 3D image.

# Be aware!You should run this example after running 'Example.py'

if __name__ == '__main__':
    # Loading original image(before running 'Example.py')
    # PS:In order to save our programs' demonstrating times,Original image(50+MiB) is replaced by its 'tag'(300+KiB)
    image_array = sitk.ReadImage('./data/Origin/COVID001.nii.gz')
    # Loading 'exampled' image(original image that already have run 'Example.py')
    connect_array = sitk.ReadImage('./data/connect_out/Origin_slice.nii.gz')

    # Getting numpy array
    img0 = sitk.GetArrayFromImage(image_array)
    img1 = sitk.GetArrayFromImage(connect_array)

    # You can change the first number to view different pieces of this two nii 3D images.
    img00 = img0[60, :, :]
    img01 = img1[60, :, :]

    # image before padding,slicing and connecting
    plt.imshow(img00, cmap='Greys_r')
    plt.show()
    print(img0.shape)

    # image after padding,slicing and connecting
    plt.imshow(img01, cmap='Greys_r')
    plt.show()
    print(img1.shape)

    # As you can see,these two 3D img is the same indicating that our tools is completely correct.
    # Thus,trained blocks' connecting accuracy can be strictly guaranteed!
