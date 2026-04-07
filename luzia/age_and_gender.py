# from https://github.com/smahesh29/Gender-and-Age-Detection
import cv2

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_list = [(0, 2), (4, 6), (8, 12), (15, 20), (25, 32), (38, 43), (48, 53), (60, 100)]
gender_list = ['male', 'female']

face_net = cv2.dnn.readNet("../models/opencv_face_detector_uint8.pb", "../models/opencv_face_detector.pbtxt")
age_net = cv2.dnn.readNet("../models/age_net.caffemodel", "../models/age_deploy.prototxt")
gender_net = cv2.dnn.readNet("../models/gender_net.caffemodel", "../models/gender_deploy.prototxt")
padding = 20


def analyze(image):
    result = {}

    face_boxes = _detect_faces(face_net, image)
    if not face_boxes:
        raise ValueError("no face detected")

    face_box = face_boxes[0]
    face = image[
           max(0, face_box[1] - padding):min(face_box[3] + padding, image.shape[0] - 1),
           max(0, face_box[0] - padding):min(face_box[2] + padding, image.shape[1] - 1)
    ]
    blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

    gender_net.setInput(blob)
    gender_preds = gender_net.forward()
    gender = gender_list[gender_preds[0].argmax()]
    result["gender"] = gender

    age_net.setInput(blob)
    age_preds = age_net.forward()
    age = age_list[age_preds[0].argmax()]
    result["age"] = age

    return result


def _detect_faces(net, frame, conf_threshold=0.7):
    frame_opencv_dnn = frame.copy()
    frame_height = frame_opencv_dnn.shape[0]
    frame_width = frame_opencv_dnn.shape[1]
    blob = cv2.dnn.blobFromImage(frame_opencv_dnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    face_boxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frame_width)
            y1 = int(detections[0, 0, i, 4] * frame_height)
            x2 = int(detections[0, 0, i, 5] * frame_width)
            y2 = int(detections[0, 0, i, 6] * frame_height)
            face_boxes.append([x1, y1, x2, y2])
    return face_boxes
