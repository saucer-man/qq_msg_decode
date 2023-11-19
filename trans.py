
from data import faceMap

import json

sortedFaceMap = sorted(faceMap.items(), key=lambda x: x[0])

dict_map = {item[0]: item[1] for item in sortedFaceMap}

# 写入 face.json

with open('face.json', 'w', encoding='utf-8') as f:
    json.dump(dict_map, f, ensure_ascii=False)
    
