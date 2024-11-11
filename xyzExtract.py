#this program extracts xyz coordinates from .RINEX files and converts them to lat lon coordinates


import os
import numpy as np
import pymap3d.ecef as ecef

#variables
fileType = ".24o"
output_name = "coordinates.txt"
xyz_coords = []
folder = "FOLDER_NAME_HERE"
folder_path = os.path.join(os.getcwd(), folder)
output_file = os.path.join(os.getcwd(), output_name)

#extracts xyz coordinates from .24o files
for file in os.listdir(folder_path):
    print(file)
    if file.endswith(fileType):
        print(file)
        with open(os.path.join(folder_path, file), "r") as f:
            lines = f.readlines()
            # Extract xyz coordinates
            for line in lines:
                rline = line.rstrip()
                if rline.endswith("XYZ"):
                    coords = rline[:-19]
                    coords2 = coords.strip()
                    xyz_coords.append(coords2)
                elif rline.endswith("NAME"):
                    stName = rline[:4]
                    xyz_coords.append(stName + " ")

#writes to file
with open(output_file, "w") as f:
    for coord in xyz_coords:
        if coord[-1].isdigit() == True:
            x, y, z = coord.split()
            lat, lon, ellip = ecef.ecef2geodetic(float(x), float(y), float(z))
            f.write(f"{lat} {lon}")
            f.write("\n")
        elif coord[-1].isdigit() == False:
            f.write(coord)