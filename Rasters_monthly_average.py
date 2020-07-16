import pandas as pd
import os
import glob
from PIL import Image
import numpy as np
import re

# import WA+ modules
import watools.General.data_conversions as DC
import watools.General.raster_conversions as RC

os.chdir(r"D:\chapter3analysis\precipitation")
#state_date = '2007-10-01'
#end_date = '2008-09-01'
in_files = '*monthly*.tif'

def monthly_to_yearly(in_files):
    
    #month_range = pd.date_range(start= state_date, end= end_date, freq= 'MS').strftime("%Y.%m").tolist()
    #print(month_range)
    
    month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    month_word = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    files = glob.glob(in_files)
    #print(files)

    # Get array information and define projection
    geo_out, proj, size_X, size_Y = RC.Open_array_info(files[0])
    if int(proj.split('"')[-2]) == 4326:
        proj = "WGS84"
    count = 0
    for i in month_list:
        files_list = []
        data = []
        for file in files:
            if re.search(".*\."+i+"\.01.*", file):
                files_list.append(file)

        for j in files_list:
            photo = Image.open(j)
            month = np.array(photo)
            data.append(month)

        #print(data)
        arr_month = np.array(data)

        month_avg = np.average(arr_month, axis=1)
        #print(month_avg)
        #print(month_avg.shape)

        # Save tiff file
        for m_index, m_word in zip(month_list, month_word):
            if m_index == i:
                DC.Save_as_tiff(r"D:\chapter3analysis\precipitation\Average\{}.tif".format(m_word), month_avg, geo_out, proj)
        
        print(month_word[count])
        count += 1


monthly_to_yearly(in_files)
