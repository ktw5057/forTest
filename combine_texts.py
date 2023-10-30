def combine_texts(texts_with_centers):
    if len(texts_with_centers) == 0:  # 텍스트가 없는 경우 빈 문자열 반환
        return ""
    count =0 #줄 번호
    line={} # 줄배분할 배열
    #한박스 안에 있는 글자 크기

    wordSize = max(texts_with_centers[0][2])-min(texts_with_centers[0][2])
    # 첫번째로 나온 글짜의 맨위 가장 작은 y값에 그 가장 작은 y값에서 글자크기만큼 더한 y값보다 작은 y값평균인 한 글자만 같은 줄로 인식한다. 이걸 while문으로 첫번쩨 단어가 안나올때까지
    while True:
        Word_y_Mi=min(texts_with_centers[0][2])# 줄에서 첫번째 단어의 y값
        #print(Word_y_Mi)
        line[count]=[""]
        for text in texts_with_centers:
            if sum(text[2]) / len(text[2]) < Word_y_Mi+wordSize:
                if(line[count]==[""]):
                    line[count]=[text]
                else:
                    line[count].append(text)
        print(line[count])
        #분리한 text와 좌표는 원래 있던 리스트에서 지운다
        for delText in line[count]:
            texts_with_centers.remove(delText)
        #print(texts_with_centers)

        #원래있던 리스트가 아무값도 없으면 while이 끝난다
        if len(texts_with_centers) == 0:
            break
        count+=1

    #print(line)

    #각 줄에서 람다 이용해서 x값 평균으로 정렬하기 -> 거의 쓸필요가 없을 느낌
    for idx in range(len(line)):
        line[idx].sort(key=lambda item:  sum(item[1]) / len(item[1]))


    # 나눴던 각줄 다시 합쳐주기
    sentences = []
    for idx in range(len(line)):
        for idx2 in range(len(line[idx])):
            sentences.append(line[idx][idx2])
    #print(sentences)
    # 텍스트들을 중심 좌표의 평균값 기준으로 정렬 sum(item[2]) / len(item[2]
    #texts_with_centers.sort(key=lambda item: (sum(item[2]) / len(item[2]), sum(item[1]) / len(item[1])))
    #texts_with_centers.sort(key=lambda item: (sum(item[2]) / len(item[2]) if  (sum(item[2]) / len(item[2])<max()))


    combined_text = sentences[0][0]
    for i in range(1, len(sentences)):
        combined_text += '' + sentences[i][0]

    return combined_text

#texts_with_centers=[["\ubc88\ud638", [61.0, 93.0, 93.0, 61.0], [68.0, 68.0, 86.0, 86.0]], ["\ub4f1\ub85d", [61.0, 92.0, 92.0, 61.0], [55.0, 55.0, 71.0, 71.0]]]
#k = combine_texts(texts_with_centers)
#print(k)