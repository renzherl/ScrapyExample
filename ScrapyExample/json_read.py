# -*- coding: utf-8 -*-

import json
from pprint import pprint
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

with open('fresh.json') as f:
    data = json.load(f)

#pprint(data)
print len(data)
with open('fresh2.json', 'w') as ff:
    for js in data:
        x = json.dumps(js, ensure_ascii=False)
        ff.write(x)
        #print x