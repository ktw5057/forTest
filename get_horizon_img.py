import os
import cv2
import numpy as np
import imageio

def get_horizon_img(image_folder, output_folder):
    for filename in os.listdir(image_folder):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.PNG'):
            img_path = os.path.join(image_folder, filename)
            img_array = np.fromfile(img_path, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 엣지 검출
            edges = cv2.Canny(img, 50, 150, apertureSize=3)

            # 허프 변환을 이용한 선분 검출, 최소 선의 길이를 크게 설정하여 가로선만 검출
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 200, minLineLength=200, maxLineGap=50)

            angle = 0
            # 검출한 선분들의 기울기를 계산하여 각도 계산, 가로선만 고려하므로 각도가 크게 벗어나는 선분은 무시
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(y2 - y1) < abs(x2 - x1): # 대각선은 무시
                    angle += np.arctan2(y2 - y1, x2 - x1)

            # 선분이 없는 경우를 대비한 예외처리
            if len(lines) != 0:
                angle /= len(lines)

            # 각도를 degree 단위로 변환
            angle = angle * 180.0 / np.pi

            # 이미지 중앙을 기준으로 각도만큼 회전
            (h, w) = img.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, \
                        borderMode=cv2.BORDER_REPLICATE)

            th1,img_bin = cv2.threshold(gray_scale,150,225,cv2.THRESH_BINARY)
            img_bin=~img_bin

            ### selecting min size as 15 pixels
            line_min_width = 15
            kernal_h = np.ones((1,line_min_width), np.uint8)
            kernal_v = np.ones((line_min_width,1), np.uint8)

            img_bin_h = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_h)
            img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_v)
            img_bin_final = img_bin_h | img_bin_v

            final_kernel = np.ones((3,3), np.uint8)
            img_bin_final = cv2.dilate(img_bin_final,final_kernel,iterations=1)

            _, labels, stats,_ = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)

            n1 = np.array(stats[2:])
            min_x = n1[:, 0].min() - 5
            min_y = n1[:, 1].min() - 5

            xw = n1[:,[0,2]].sum(axis=1).max(0)
            xw = xw + 5
            yh = n1[:,[1,3]].sum(axis=1).max()
            yh = yh + 5

            # 이미지 크롭
            cropped_image = rotated[min_y:yh, min_x:xw]

            # 결과 이미지를 다른 이름으로 저장
            output_path = os.path.join(output_folder, filename)
            imageio.imwrite(output_path, cropped_image)

            print(f"Processed image saved to {output_path}")


