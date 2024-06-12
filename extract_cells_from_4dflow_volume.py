import pyvista as pv
from pathlib import Path
import os
from os.path import join

# this is a segmentation of the aorta in nrrd (volumetric segmentation)
aorta_seg = pv.read('./extracted_4dflow_Kowal_RM/segmentations/segmentation_aorta_pcmra_enlarged.nrrd')
aorta_seg = aorta_seg.point_data_to_cell_data()

# these are the indices of the cells which are insiede the aorta
aorta_idxs = aorta_seg['ImageScalars']>0

# iterate. through the processed 4dflow volumes and extract only cells inside the aorta
inputDir = './extracted_4dflow_Kowal_RM/flow/'
for ii, (root, dirs, files) in enumerate(os.walk(inputDir)):
    for file in files:
        print(ii,file)
        flow = pv.read(join(root,file))
        flow = flow.extract_cells(aorta_idxs)
        # save unstructured grid files with only these cells
        flow.save(join(root, file.replace('TEST_CASE', 'unstr')))
