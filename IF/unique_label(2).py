import pandas as pd

# 파일 경로 설정
file_path = r'C:\Users\NetDB\Desktop\RTP2\IF\anomaly_score_labeled.csv'

# CSV 파일 불러오기
data = pd.read_csv(file_path)

# 각 grid_label별로 -1과 1의 개수 계산
grid_label_counts = data.groupby(['grid_label', 'anomaly']).size().unstack(fill_value=0)

# -1이 하나라도 있으면 -1로 설정
grid_label_counts['final_decision'] = grid_label_counts.apply(lambda row: -1 if row[-1] >= 1 else 1, axis=1)

# 최종 결정값을 원래 데이터에 반영
data['F1'] = data['grid_label'].map(grid_label_counts['final_decision'])

# 최종 결과 파일로 저장
output_file_path = r'C:\Users\NetDB\Desktop\RTP2\IF\final_anomaly_decision.csv'
data[['lat', 'lng', 'F1','grid_label']].to_csv(output_file_path, index=False)

output_file_path
