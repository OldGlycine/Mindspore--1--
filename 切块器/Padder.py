import numpy as np


class Padder:
    r"""
    Usually,we use nibabel or SITK to load a 3D image as a numpy array.
    Here's a tool that can pad 0 to 3D image array with customized DWH(pixels) and erase all the zeros in the same padded-image.
    You need to give 4 parameter:

    img : Your 3D image array,its arrangement must be 'DWH'.So we strongly suggest load image by SITK!

    D : Each block's Depth

    W : Each block's Width

    H : Each block's Height
    """

    def __init__(self, img, D, W, H):
        self.H = H
        self.W = W
        self.D = D
        self.pad_H = 0
        self.pad_W = 0
        self.pad_D = 0
        self.img = img

    def Padding(self):
        if self.img.shape[0] < self.D:
            pad = self.D - self.img.shape[0]
            self.pad_D += pad
            padding = np.zeros([pad, self.img.shape[1], self.img.shape[2]])
            self.img = np.concatenate((padding, self.img), axis=0)
        if self.img.shape[1] < self.W:
            pad = self.W - self.img.shape[1]
            self.pad_W += pad
            padding = np.zeros([self.img.shape[0], pad, self.img.shape[2]])
            self.img = np.concatenate((padding, self.img), axis=1)
        if self.img.shape[2] < self.H:
            pad = self.H - self.img.shape[2]
            self.pad_H += pad
            padding = np.zeros([self.img.shape[0], self.img.shape[1], pad])
            self.img = np.concatenate((padding, self.img), axis=2)

        if self.img.shape[0] % self.D != 0:
            pad = self.D - (self.img.shape[0] % self.D)
            self.pad_D += pad
            padding = np.zeros([pad, self.img.shape[1], self.img.shape[2]])
            self.img = np.concatenate((padding, self.img), axis=0)
        if self.img.shape[1] % self.W != 0:
            pad = self.W - (self.img.shape[1] % self.W)
            self.pad_W += pad
            padding = np.zeros([self.img.shape[0], pad, self.img.shape[2]])
            self.img = np.concatenate((padding, self.img), axis=1)
        if self.img.shape[2] % self.H != 0:
            pad = self.H - (self.img.shape[2] % self.H)
            self.pad_H += pad
            padding = np.zeros([self.img.shape[0], self.img.shape[1], pad])
            self.img = np.concatenate((padding, self.img), axis=2)
        return self.img

    # Here you need to give one parameter 'img'
    # img : A 3D image array that already padded
    # WARNING! One Padder only have one padding rule.
    def DePadding(self, img):
        img = img[self.pad_D:, self.pad_W:, self.pad_H:]
        return img

    # Function that return the lines of padding zeros for further depadding
    def getPadDHW(self):
        return [self.pad_D, self.pad_W, self.pad_H]

    # Function that set depadding rules
    def setPadDHW(self, depadding):
        self.pad_D = depadding[0]
        self.pad_W = depadding[1]
        self.pad_H = depadding[2]


'''
Here lies an example about how to use the Padder!
'''
if __name__ == '__main__':
    # Suppose that we have a 3D image with height:33 width:12 depth:16
    arr = np.zeros([21, 13, 48])
    # (16, 12, 33)
    print(arr.shape)

    # Creating Padder
    # We want to slice the arr with a block sized (7,13,16)
    # According to the padder's code,arr's shape will be (21, 13, 48) after padding
    p = Padder(arr, 7, 13, 16)

    # Beginning padding
    arr = p.Padding()
    # Get depadding rules [5, 1, 15]
    depadding = p.getPadDHW()
    print(depadding)
    # Now we get arr with (21, 13, 48).Correct!
    print(arr.shape)
    print('------------------------------------')
    # Depad
    arr = p.DePadding(arr)
    # (16, 12, 33).Correct!
    print(arr.shape)
    print('------------------------------------')
    # As you can see,padder pads '0' which 'covering' the original arr
    print(arr)
