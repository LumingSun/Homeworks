import numpy as np
import pandas as pd
import io
import bson                       # this is installed with the pymongo package
import matplotlib.pyplot as plt
from PIL import Image
import multiprocessing as mp      # will come in handy due to the size of the data


data = bson.decode_file_iter(open('G:\AICompetition\input\\train_example.bson', 'rb'))
prod_to_category = dict()

for c, d in enumerate(data):
    product_id = d['_id']
    category_id = d['category_id']         # This won't be in Test data
    prod_to_category[product_id] = category_id
    for e, pic in enumerate(d['imgs']): #e是某件的图片数量
        picture = Image.open(io.BytesIO(pic['picture']))
        img_array = np.array(picture)
        # print(img_array.shape)
        # img_string = img_array.tostring()
        list_array = np.ravel(img_array)
        new = str(product_id) + '\t' + str(list_array.tolist())+'\n'
        out_path = '.\data\\'+ str(category_id) + '.txt'
        f_handle = open(out_path, 'a')
        f_handle.write(new)
        f_handle.close()
        # print(new)
        # print(np.reshape(new,[180,180,3]))
        # print(np.fromstring(img_string,dtype=np.uint8))
        break


prod_to_category = pd.DataFrame.from_dict(prod_to_category, orient='index')
# prod_to_category.index.name = '_id'
prod_to_category.rename(columns={0: 'category_id'}, inplace=True)
print(prod_to_category)
#picture.show()
# plt.imshow(picture)
# plt.show()

