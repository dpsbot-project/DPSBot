# -*- coding: utf-8 -*-

"""Inception v3 architecture 모델을 retraining한 모델을 이용해서 이미지에 대한 추론(inference)을 진행하는 예제"""
# 를 디스코드 봇에 쓰려고 수정 모듈

import numpy as np
import tensorflow as tf
import cv2
import sys
import os.path
from pathlib import Path
from PIL import Image


def detect(filename, id, cascade_file="./lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)
    list = []

    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor=1.1,
                                     minNeighbors=5,
                                     minSize=(24, 24))
    imgNum = 0
    ext = "png"
    for (x, y, w, h) in faces:
        cropped = image[y - int(h / 4):y + h + int(h / 4), x -
                    int(w / 4):x + w + int(w / 4)]
        # 이미지를 저장
        imgNum += 1
        cv2.imwrite(id + str(imgNum) + '.' + ext, cropped)
        list.append(id + str(imgNum) + '.' + ext)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imwrite("out.png", image)
    return list

# 추론을 진행할 이미지 경로
# 읽어들일 graph 파일 경로
modelFullPath = 'D:/tmp/output_graph.pb'
# 읽어들일 labels 파일 경로
labelsFullPath = 'D:/tmp/output_labels.txt'


def create_graph():
    """저장된(saved) GraphDef 파일로부터 graph를 생성하고 saver를 반환한다."""
    # 저장된(saved) graph_def.pb로부터 graph를 생성한다.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

def run_inference_on_image(filelist):
    if filelist is not []:
        parent_list = []
        i = 0
        for imagePath in filelist:
            answer = None
            if not tf.gfile.Exists(imagePath):
                tf.logging.fatal('File does not exist %s', imagePath)
                return answer
            try:
                image_context = Image.open(imagePath)
                image_array = np.array(image_context)[:, :, 0:3]  # Select RGB channels only.
            except:
                raise
            # 저장된(saved) GraphDef 파일로부터 graph를 생성한다.
            create_graph()

            with tf.Session() as sess:
                softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
                predictions = sess.run(softmax_tensor,
                                       {'DecodeJpeg:0': image_array})
                predictions = np.squeeze(predictions)
                # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.
                top_k = predictions.argsort()[-5:][::-1]
                f = open(labelsFullPath, 'rb')
                lines = f.readlines()
                labels = [str(w).replace("\n", "") for w in lines]
                for node_id in top_k:
                    human_string = labels[node_id]
                    score = predictions[node_id]
                    print('%s (score = %.5f)' % (human_string, score))
                print("=" * 25)
                list2 = []
                name = labels[top_k[0]].replace(
                    "\\n", "").replace("b'", "").replace("'", "")
                list2.append(labels[top_k[0]].replace(
                    "\\n", "").replace("b'", "").replace("'", ""))
                answer = labels[top_k[0]].replace(
                    "\\n", "").replace("b'", "").replace("'", "")
                # remove or put some
                if answer == "nishikino maki":
                    answer = "니시키노 마키"
                elif answer == "takami chika":
                    answer = "타카미 치카"
                elif answer == "yazawa nico":
                    answer = "야자와 니코"
                elif answer == "shimamura uzuki":
                    answer = "시마무라 우즈키"
                elif answer == "hatsune miku":
                    answer = "하츠네 미쿠"
                elif answer == "tsushima yoshiko":
                    answer = "츠시마 요시코"
                elif answer == "kousaka honoka":
                    answer = "코우사카 호노카"
                elif answer == "minami kotori":
                    answer = "미나미 코토리"
                elif answer == "yonebayashi saiko":
                    answer = "요네바야시 사이코"
                elif answer == "shibuya rin":
                    answer = "시부야 린"
                elif answer == "sonoda umi":
                    answer = "소노다 우미"
                elif answer == "ayase eli":
                    answer = "아야세 에리"
                elif answer == "tojo nozomi":
                    answer = "토조 노조미"
                elif answer == "watanabe you":
                    answer = "와타나베 요우"
                elif answer == "koizumi hanayo":
                    answer = "코이즈미 하나요"
                elif answer == "hoshizora rin":
                    answer = "호시조라 린"
                elif answer == "kanzaki ranko":
                    answer = "칸자키 란코"
                num = predictions[top_k[0]] * 100
                score = "%.1f" % num
                list2.append(answer)
                list2.append(score)
                list2.append(imagePath)
                image_data = tf.gfile.FastGFile(
                                imagePath, 'rb').read()
                with open("D:/retrain/pending/%s/%s" % (name, imagePath), "wb") as w:
                    w.write(image_data)
                parent_list.append(list2)
                i += 1
        return parent_list
    else:
        return None

def findfaceanddetect(filename, id):
    return run_inference_on_image(detect(filename, id))
