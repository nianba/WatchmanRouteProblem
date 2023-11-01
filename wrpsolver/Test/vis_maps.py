import os
import json
import numpy as np

def GetPolygon(seed):
    json_path = os.path.dirname(os.path.abspath(__file__))+"/json/"
    map_file = os.path.dirname(os.path.abspath(__file__))+"/map_id_35000.txt"
    map_ids = np.loadtxt(map_file, str)

    file_name = map_ids[seed]
    # print(file_name)
    with open(json_path + '/' + file_name + '.json') as json_file:
        json_data = json.load(json_file)


    # bbox = json_data['bbox']
    # maxNum = max(bbox['max'][0],bbox['max'][1])
    # verts = (np.array(json_data['verts']) * meter2pixel / math.ceil(maxNum)).astype(int)
    verts = np.array(json_data['verts'])*10
    return verts,file_name,json_data['room_num']