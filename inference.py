from sklearn.preprocessing import LabelEncoder
import torch
from transformers import BertTokenizer, BertForSequenceClassification

class BertModelInference:
    def __init__(self, model_path, tokenizer_name='bert-base-uncased', label_classes=None, max_len=128, device=None):
        """
        BERT 모델 로드 및 초기화
        """
        self.model_path = model_path
        self.tokenizer_name = tokenizer_name
        self.max_len = max_len
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.label_encoder = LabelEncoder()

        if label_classes:
            self.label_encoder.fit(label_classes)  # 클래스 정보 설정

        # 모델 및 토크나이저 로드
        self.model = self._load_model()
        self.tokenizer = self._load_tokenizer()

    def _load_model(self):
        """전체 모델 객체 로드"""
        model = torch.load(self.model_path, map_location=self.device)
        model.to(self.device)
        model.eval()
        return model


    def _load_tokenizer(self):
        """토크나이저 로드"""
        return BertTokenizer.from_pretrained(self.tokenizer_name)

    def preprocess(self, texts):
        """입력 텍스트 전처리"""
        return self.tokenizer(
            texts,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

    def predict(self, texts):
        """
        입력 텍스트 리스트에 대한 예측
        """
        # 데이터 전처리
        preprocessed_data = self.preprocess(texts)
        input_ids = preprocessed_data['input_ids'].to(self.device)
        attention_mask = preprocessed_data['attention_mask'].to(self.device)

        # 모델 추론
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            _, predictions = torch.max(outputs.logits, dim=1)

        # 정수형 레이블과 디코딩된 레이블 반환
        int_labels = predictions.cpu().numpy()
        decoded_labels = self.label_encoder.inverse_transform(int_labels)
        return int_labels, decoded_labels
