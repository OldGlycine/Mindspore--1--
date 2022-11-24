import glob
import os
import SimpleITK as sitk
from Padder import *


class Connector:
    r"""
    We have already sliced some blocks and sent them to our nets to train. Now we need to connect these blocks with
    connecting rule which is the same as padding rules and slicing rules we have already give to slicer and padder.
    Thus,Connector's parameter 'Rule' relies on Slicer.

    connect_path : The path of blocks' location.

    Rule : Connecting rules,you can get them by Slicer's function named 'getXYZ()'.

    DePadding : Depadding rules,you can use Padder's function 'getPadDHW'
    """

    def __init__(self, connect_path, Rule, DePadding):
        super(Connector, self).__init__()
        self.connect_path = connect_path
        self.rule = Rule
        self.depadding = DePadding

    def Connector(self):
        push = 0
        for Path in self.connect_path:
            savepath = Path.replace('Origin_slice', 'connect_out')
            savepath = savepath.replace('Tag_slice', 'connect_out')
            savepath = savepath.replace('.nii', '_connect.nii')
            if not os.path.exists(savepath):
                os.makedirs(savepath)
                print("Created ouput directory: " + savepath)
            print("now we are connecting:" + Path.split('/')[2])
            filepath = glob.glob(os.path.join(Path, '*.nii.gz'))
            filepath.sort()
            Darr = np.array(None)
            HDarr = np.array(None)
            WHDarr = np.array(None)
            counter = 0
            for W in range(self.rule[0]):
                for H in range(self.rule[1]):
                    for D in range(self.rule[2]):
                        block = sitk.ReadImage(filepath[counter])
                        block = sitk.GetArrayFromImage(block)
                        print('loading:' + filepath[counter])
                        print('loading successfully:' + str(counter + 1))
                        if Darr.size == 1:
                            Darr = block
                            counter += 1
                        else:
                            Darr = np.vstack((Darr, block))
                            counter += 1
                    if HDarr.size == 1:
                        HDarr = Darr
                        Darr = np.array(None)
                    else:
                        HDarr = np.hstack((HDarr, Darr))
                        Darr = np.array(None)
                if WHDarr.size == 1:
                    WHDarr = HDarr
                    HDarr = np.array(None)
                else:
                    WHDarr = np.dstack((WHDarr, HDarr))
                    HDarr = np.array(None)
            data = WHDarr

            depadder = Padder(data, self.depadding[0], self.depadding[1], self.depadding[2])
            depadder.setPadDHW(self.depadding)
            data = depadder.DePadding(data)

            data = sitk.GetImageFromArray(data)
            sitk.WriteImage(data, savepath + '/' + Path.split('/')[2] + '.nii.gz')
            print("saving as" + savepath)
            print("push next...")
            push += 1


if __name__ == '__main__':
    # Slicer's two 'get' function return results as follows:
    # path:['./data/Origin_slice', './data/Tag_slice']
    # Rule:[4, 4, 10]
    # Padder's 'get' function return result as follows:
    # DePadding:[12, 0, 0]
    path = ['./data/Origin_slice', './data/Tag_slice']
    Rule = [4, 4, 10]
    print(Rule)
    DePadding = [12, 0, 0]
    c = Connector(path, Rule, DePadding)
    # Start to connect our blocks
    c.Connector()
    # The result can be found in ./data/connect_out
