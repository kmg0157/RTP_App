from inference import BertModelInference

# 초기화
model_path = 'bert_model.pth'
label_classes = ['N', 'AN']  # 학습 데이터에서 사용한 클래스
bert_inference = BertModelInference(model_path=model_path, label_classes=label_classes)

# 예시 데이터
example_data = [    
    "KECABBAB KECABBAA KECABBAB", # N  
    "KECABBCD KECABBCB KECABADB KECABADD KECABADC KECABACD KECABACC KECABCAA KECABCAB KECABCBA KECADADD KECCBAAC KECCBACA KECCBACD",  # N
    "JEADBDDC JEBCCCDC", # AN            
    "KECABBAB KECABBAA", # N
    "IGACABBC IGACABAD", # AN
    "KECABBAB KECABBAA HGFEDCBA IJKLMNOP", # N + 가짜(X)
    "KFBABDDA KFBABDBA", # AN
    "ABCDEFGH IJKLMNOP", # 가짜
    "ABCDEFGH IJKLMNOP GJDAADCD", # 가짜 + AN
    "ABCDEFGH IJKLMNOP KECABBAA",
    "GJDAADCD", # AN
    "KECABBAA" # N
]

# 추론 수행
int_labels, decoded_labels = bert_inference.predict(example_data)

print("Decoded Labels:", decoded_labels)  # 디코딩된 레이블
