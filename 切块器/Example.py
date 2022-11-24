from Connector import *
from Slicer import *

# Here's an example demonstrating our 3 tools' usage.
# Just 4 lines to access! Easy to use!
if __name__ == '__main__':
    # Type in the path of your original big 3D images and wanted DHW of each blocks
    # WARNING ! Original images and its masks MUST be saved in './data/Origin' and './data/Tag'
    slicer = Slicer('./data/', 16, 128, 128)  # Line 1
    slicer.Slicer()  # Line 2
    print('---------------------------------------')

    # Connector's parameters can be got from slicer!
    connector = Connector(slicer.getTestPath(), slicer.getXYZ(), slicer.getPadDHW())  # Line 3
    connector.Connector()  # Line 4
    print('---------------------------------------')

    print('Successfully completed!')
