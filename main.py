from io import StringIO
from pathlib import Path
import streamlit as st
import time
from detect import main_detect
import os
import sys
import argparse
from PIL import Image

def get_subdirs(b='.'):
    '''
        获取路径
    '''
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


def get_detection_folder():
    '''
        获取最新预测结果
    '''
    return max(get_subdirs(os.path.join('runs', 'detect')), key=os.path.getmtime)


if __name__ == '__main__':

    st.title('YOLOv5 手写数字识别')#正文大标题

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='weights/weights1.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default='data/Samples/tests/', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--data', type=str, default='data/writenum.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')

    opt = parser.parse_args()#感觉不用动，上传图片自动添加到image
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    #print(opt)

    source2 = ("yolov5l", "yolov5s")
    source_index2 = st.sidebar.selectbox("选择模型", range(
        len(source2)), format_func=lambda x: source2[x])#下拉选择框 0-选项1 1-选项2 ...

    if source_index2 == 0:
        opt.weights = f'weights/weights1.pt'#修改source参数
        #print("labels 2")
    else:
        opt.weights = f'weights/weights2.pt'#修改source参数

    source1 = ("图片检测", "视频检测")
    source_index1 = st.sidebar.selectbox("选择检测对象", range(
        len(source1)), format_func=lambda x: source1[x])#下拉选择框 0-选项1 1-选项2 ...

    if source_index1 == 0:        
        uploaded_file = st.sidebar.file_uploader(#上传文件选择框
            "上传图片", type=['png', 'jpeg', 'jpg'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='资源加载中...'):
                st.sidebar.image(uploaded_file)
                picture = Image.open(uploaded_file)
                picture = picture.save(f'data/Samples/images/{uploaded_file.name}')#存到image文件夹
                opt.source = f'data/Samples/images/{uploaded_file.name}'#修改source参数
                #print("labels 2")
        else:
            is_valid = False
    else:
        uploaded_file = st.sidebar.file_uploader("上传视频", type=['mp4'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='资源加载中...'):
                st.sidebar.video(uploaded_file)
                with open(os.path.join("data", "Samples", "videos", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                opt.source = f'data/Samples/videos/{uploaded_file.name}'
        else:
            is_valid = False
    
    if st.button('使用测试集测试'):
        st.write('已加载测试图片集')
        opt.source = f'data/Samples/tests/'
        
        main_detect(opt)
        #print('结束')
        with st.spinner(text='Preparing Images'):
            for img in os.listdir(get_detection_folder()):
                st.image(str(Path(f'{get_detection_folder()}') / img))

            st.balloons()

    print(opt)

    if is_valid:#有效，可以检测
        print('valid')

        if st.button('开始检测'):

            #print('开始')
            #print(opt)
            main_detect(opt)
            #print('结束')

            if source_index1 == 0:#图片选项
                with st.spinner(text='Preparing Images'):
                    for img in os.listdir(get_detection_folder()):
                        st.image(str(Path(f'{get_detection_folder()}') / img))

                    st.balloons()
            else:
                with st.spinner(text='Preparing Video'):
                    for vid in os.listdir(get_detection_folder()):
                        st.video(str(Path(f'{get_detection_folder()}') / vid))

                    st.balloons()
    

