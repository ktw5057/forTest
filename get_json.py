import os
import requests
import uuid
import time
import json

def get_json(image_folder, json_folder, api_url, secret_key):
    headers = {'X-OCR-SECRET': secret_key}

    for filename in os.listdir(image_folder):
        # 이미지 파일만 선택
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.PNG'):
            image_file_path = os.path.join(image_folder, filename)

            # OCR API에 전송
            request_json = {
                'images': [
                    {
                        'format': 'PNG',
                        'name': filename
                    }
                ],
                'requestId': str(uuid.uuid4()),
                'version': 'V2',
                'timestamp': int(round(time.time() * 1000))
            }
            payload = {'message': json.dumps(request_json).encode('UTF-8')}
            files = [('file', open(image_file_path, 'rb'))]
            response = requests.post(api_url, headers=headers, data=payload, files=files)

            # 리스폰스 JSON 파일로 저장
            response_json = json.loads(response.text)
            json_file_path = os.path.join(json_folder, os.path.splitext(filename)[0] + '.json')
            with open(json_file_path, 'w', encoding='UTF-8') as f:
                json.dump(response_json, f, indent=4, ensure_ascii=False)

            print(f'Response saved to {json_file_path}')