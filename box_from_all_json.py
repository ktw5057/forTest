import os
import json
from combine_texts import combine_texts
from json_preprocessor import preprocess_json_in_folder

def get_texts_in_boxes_from_all_jsons(json_folder_path, selected_boxes_info):
    # 폴더 내의 모든 파일에 대해
    for filename in os.listdir(json_folder_path):
        # .json 파일인 경우만 처리합니다.
        if filename.endswith(".json"):
            json_file_path = os.path.join(json_folder_path, filename)
            
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
            preprocessed_data = preprocess_json_in_folder(json_data)

            # 각 선택된 박스에 대해
            for box_info in selected_boxes_info:
                texts_in_box = []
                for text, x_coordinates, y_coordinates in preprocessed_data:
                    center_x = sum(x_coordinates) / len(x_coordinates)
                    center_y = sum(y_coordinates) / len(y_coordinates)

                    #삭제

                combined_text = combine_texts(texts_in_box)
                box_info['text'] = combined_text  # 업데이트된 텍스트를 저장합니다.

            print(f"Updated text in selected boxes for file: {filename}")

            return selected_boxes_info
