import glob
import os
import SimpleITK as sitk
from Padder import *

global data


class Slicer:
    r"""
    After padding,we need to cut the 3D image into pieces with cutting rules.
    This is a Slicer that can slice our 3D image array.
    PS:Slicer contains Padder.
    You need to give 2 parameter:

    filepath : The path where your 3D image lies.

    DHW : Your Padder's DHW.

    After slicing,you can send them to your nets to train.
    """
    def __init__(self, filepath, D, H, W):
        super(Slicer, self).__init__()
        self.p = None
        self.filepath = filepath
        self.D = D
        self.H = H
        self.W = W
        self.x = 0
        self.y = 0
        self.z = 0
        self.TestPath = []
        self.xyz = []


    def Slicer(self):
        slice_counter = 0
        path = ['Origin/*.nii.gz', 'Origin_slice', 'Tag/*.nii.gz',
                'Tag_slice']
        i = 0
        for _ in range(0, 2):
            inputfiles = glob.glob(os.path.join(self.filepath, path[i]))
            outputfile = self.filepath + path[i + 1]
            inputfiles.sort()

            i += 2

            print('Input file is ', inputfiles)
            print('Output folder is ', outputfile)

            for inputfile in inputfiles:
                print("Slicing:", inputfile)
                image_array = sitk.ReadImage(inputfile)
                image_array = sitk.GetArrayFromImage(image_array)
                self.p = Padder(image_array, self.D, self.H, self.W)
                image_array = self.p.Padding()
                # print(image_array.shape) ------ (148, 512, 512) ---> (160, 512, 512)
                lenx = image_array.shape[2]
                leny = image_array.shape[1]
                lenz = image_array.shape[0]

                self.TestPath.append(outputfile)
                if not os.path.exists(outputfile):
                    os.makedirs(outputfile)
                    print("Created ouput directory: " + outputfile)
                print('Reading NIfTI file...')

                slice_x = lenx // self.W
                slice_y = leny // self.H
                slice_z = lenz // self.D

                self.x = slice_x
                self.y = slice_y
                self.z = slice_z

                if not self.xyz:
                    self.xyz.append(slice_x)
                    self.xyz.append(slice_y)
                    self.xyz.append(slice_z)

                if (slice_counter % 1) == 0:
                    for x in range(0, slice_x):
                        for y in range(0, slice_y):
                            for z in range(0, slice_z):
                                data = image_array[z * 16:(z + 1) * 16,
                                       y * 128:(y + 1) * 128,
                                       x * 128:(x + 1) * 128]
                                if (slice_counter % 1) == 0:
                                    print('Saving image...')
                                    image_name = "Slice_Piece_" + "{:0>4}".format(str(slice_counter + 1)) + ".nii.gz"
                                    slice_counter += 1
                                    nii_file = sitk.GetImageFromArray(data)
                                    sitk.WriteImage(nii_file, outputfile + '/' + image_name)  # 第二个参数 为保存路径
                                    print('Saved.')
            slice_counter = 0

        print('Finished converting images')

    # Function that return the number of the blocks in 3 dimension (DHW)
    def getXYZ(self):
        print("returning slice_x,y,z...")
        return self.xyz

    # Function that return the path of sliced blocks
    def getTestPath(self):
        print("returning TestPath...")
        return self.TestPath

    # Function that return the lines of padding zeros for further depadding
    def getPadDHW(self):
        return self.p.getPadDHW()


if __name__ == '__main__':
    # We have an example(a COVID infected lung's 3D image) lies in certain path.
    # ./data/Origin/    and    ./data/Tag
    s = Slicer('./data/', 16, 128, 128)
    # Starting slicing process.
    s.Slicer()

    # You can get 3D images' slicing saving path by this function.
    path = s.getTestPath()
    # You can get DHW rules by this function.
    rule = s.getXYZ()
    print(rule)
    # You can get deppadding rules by this function
    deRule = s.getPadDHW()

    # The results can be found in ./data/Tag_slice    and   ./data/Origin_slice
