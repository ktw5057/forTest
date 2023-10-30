import pandas as pd
import os

def output_texts_to_excel(box_texts_by_file, folder_path):
    # 빈 데이터프레임을 생성합니다.
    df = pd.DataFrame()

    # 각 파일에 대한 박스 텍스트들을 데이터프레임에 추가합니다.
    for file_name, box_texts in box_texts_by_file.items(): #
        text = []
        for box_text in box_texts:
            text.append(box_text['text'])

        # 파일 이름과 text를 포함하는 데이터프레임을 생성합니다.
        new_row = pd.DataFrame([text], columns=['Column'+str(i+1) for i in range(len(text))])
        new_file_name = file_name.replace('_processed.json', '')
        new_row.insert(0, 'File_Name', new_file_name) # 파일 이름을 첫 번째 열로 추가합니다.

        df = pd.concat([df, new_row], ignore_index=True)

    # 데이터프레임을 엑셀 파일로 저장합니다.
    excel_file_name = 'output.xlsx'
    excel_file_path = os.path.join(folder_path, excel_file_name)
    df.to_excel(excel_file_path, index=False)

    print('엑셀파일 저장 완료')
