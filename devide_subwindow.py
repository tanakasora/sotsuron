from skimage import io
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from skimage import img_as_float
import numpy as np

def first_input():
    #to get file name [list] from input.txt
    imgfilelist = open('input.txt').read()
    open('input.txt').close()
    imgfiles = imgfilelist.split()
    writerfiles = open('writer_id.txt').read()
    open('writer_id.txt').close()
    writerids = writerfiles.split()
    return imgfiles, writerids

def writers():
    writerids = first_input()[1]
    return writerids


def line(img, x=0, y=0):
    fline = x
    eline = img.shape[1]-x

    for x in range(img.shape[1]):
       for y in range(img.shape[0]):
           if img[y,x]!=255:
               fline = x
               break
           else : continue
       if img[y,x]!=255 : break
       else :
           fline = x
           continue

    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            if img[-y,-x]!=255:
                eline = img.shape[1]-x
                break
            else : continue
        if img[-y,-x]!=255 : break
        else :
            eline = img.shape[1]-x
            continue
    return fline,eline

def point(img, x=0,y=0):
    first, end = line(img)
    fcood = y
    ecood = img.shape[0]-y

    for y in range(img.shape[0]):
        for x in range(first, end-1):
            if img[y,x]!=255:
                fcood = y
                break
            else : continue
        if img[y,x]!=255 : break
        else :
            fcood = y
            continue

    for y in range(img.shape[0]):
        for x in range(first, end-1):
            if img[-y,-x]!=255:
                ecood = img.shape[0]-y
                break
            else : continue
        if img[-y,-x]!=255 : break
        else :
            ecood = img.shape[0]-y
            continue
    return fcood,ecood

def count(array):
    count = 0
    for x in range(array.shape[1]):
        for y in range(array.shape[0]):
            if array[y,x] <100:
                array[y,x] = 0
                count = count +1
            else :array[y,x]=255
    if count*100/array.size > 20:
        return True
    else : return False

def divide(img,windowsize):
    fx,ex = line(img)
    fy,ey = point(img)
    imagelist = []

    ex = ex + (ex-fx)%windowsize
    ey = ey + (ey-fy)%windowsize

    for y in range(fy, ey-windowsize, windowsize):
      for x in range(fx, ex-windowsize, windowsize):
          #print(img[y:y+windowsize,x:x+windowsize])
          tmp = img[y:y+windowsize,x:x+windowsize]
          if count(tmp)==True and tmp.shape == (windowsize,windowsize):
              imagelist.append(tmp)
    return imagelist

def each_devide():
    filename = first_input()[0][0:20]##all not[0:1]
    writerid = first_input()[1]
    writer_num = sorted(set(writerid))
    #print (filename)
    #file = open('subwindow.xml','w')
    prev_writer=999
    images =[]
    d = dict()
    for image, writer in zip(filename, writerid):
        img_array = io.imread(image)
        fx,ex = line(img_array)
        fy,ey = point(img_array)
        img = img_array[fy:ey,fx:ex]
        imagelist = (divide(img,13))
        if writer in d.keys():
            d[writer].append(imagelist)
        else:
            d[writer] = [imagelist]
    return d

def subimagelists_of_writer():
    d = each_devide()
    r = reduce(lambda a,b: np.concatenate((a,b)), d["011"])
    return r

        #np.save('subwindow',imagelist)
        #file.write(imagelist)
    #file.close()

writerid = first_input()[1]
writer_num = set(writerid)
writer_num = sorted(writer_num)


#img_array = io.imread('a01-000u-01.tif')
#fx,ex = line(img_array)
#fy,ey = point(img_array)
#img = img_array[fy:ey,fx:ex]
#imagelist = (divide(img_array,13))
#np.save('subwindow01',imagelist)
#print(imagelist)

#each_devide()
