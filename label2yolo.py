#! /usr/bin/python
# -*- coding:UTF-8 -*-


w = 640
h = 640

def convert(size, box): # size:(原图w,原图h) , box:(xmin,xmax,ymin,ymax)
    dw = 1./size[0]     # 1/w
    dh = 1./size[1]     # 1/h
    x = (box[0] + box[1])/2.0   # 物体在图中的中心点x坐标
    y = (box[2] + box[3])/2.0   # 物体在图中的中心点y坐标
    w = box[1] - box[0]         # 物体实际像素宽度
    h = box[3] - box[2]         # 物体实际像素高度
    x = x*dw    # 物体中心点x的坐标比(相当于 x/原图w)
    w = w*dw    # 物体宽度的宽度比(相当于 w/原图w)
    y = y*dh    # 物体中心点y的坐标比(相当于 y/原图h)
    h = h*dh    # 物体宽度的宽度比(相当于 h/原图h)
    return (x, y, w, h)    # 返回 相对于原图的物体中心点的x坐标比,y坐标比,宽度比,高度比,取值范围[0-1]


def convert_annotation(tmp):
    out_file = open('/root/yolo/data/labels/%06d.txt' % tmp, 'w', encoding='utf-8')
   #print(line,end=' ')
    val = line.split(' ')
    #print(val)
    imax = len(val)
    #print(imax)
    for i in range (0, imax-1 -5, 5):
        #print(str(val[i])+' '+str(val[i+1]))
        b = (float(val[i+1]), float(val[i+3]), float(val[i+2]), float(val[i+4]))
        #print(b)
        #print( xmin, ymin, xmax, ymax )
        bb = convert((w, h), b)
        #print(bb)
        out_file.write(str(val[i]) + " " + " ".join([str(a) for a in bb]) + '\n')
    #print(val[imax-6], val[imax-5], val[imax-4], val[imax-3],val[imax-2])
    b = (float(val[imax-5]), float(val[imax-3]), float(val[imax-4]), float(val[imax-2]))
    bb = convert((w, h), b)
    #print(bb)
    out_file.write(str(val[imax-6]) + " " + " ".join([str(a) for a in bb]) + '\n')

tmp = 0
labels = open('/root/yolo/data/labels.txt')
line = labels.readline()

while line:
    tmp += 1
    #print(tmp)
    convert_annotation(tmp)
    line = labels.readline()

labels.close()

'''
for index, line in enumerate(open('labels.txt', 'r'), 1):
    with open('./labels/%06d.txt' % index, 'w+') as tmp:
        tmp.write(line)
'''

