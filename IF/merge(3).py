import os
import pandas as pd

# 폴더 경로 설정 (tracking 폴더 경로)
folder_path = r'C:\Users\NetDB\Desktop\RTP2\tracking\___ecfd1086a6934ae08b555b3ae880d31e'
second_file_path = r'C:\Users\NetDB\Desktop\RTP2\IF\final_anomaly_decision.csv'
output_folder = r'C:\Users\NetDB\Desktop\RTP2\IF\output_folder'  # 처리된 파일들을 저장할 폴더

# anomaly_score_labeled.csv 파일 불러오기
data_2 = pd.read_csv(second_file_path)

# 출력 폴더가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 폴더 내 모든 CSV 파일 처리
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # 각 파일 경로 설정
        first_file_path = os.path.join(folder_path, file_name)
        
        # 첫 번째 파일 불러오기
        try:
            data_1 = pd.read_csv(first_file_path)
            print(f"{file_name} 파일이 성공적으로 읽혔습니다.")
        except Exception as e:
            print(f"{file_name} 파일을 읽는 중 오류 발생: {e}")
            continue  # 오류가 발생한 파일을 건너뜀
        
        # 파일에 lat과 lng가 있는지 확인
        if 'lat' not in data_1.columns or 'lng' not in data_1.columns:
            print(f"{file_name} 파일에 'lat' 또는 'lng' 열이 없습니다.")
            continue
        
        # 첫 번째 파일과 두 번째 파일을 'lat'과 'lng'를 기준으로 병합
        merged_data = pd.merge(data_1[['lat', 'lng']], data_2[['lat', 'lng', 'F1', 'grid_label']], on=['lat', 'lng'], how='left')
        
        # 병합 결과 확인
        if merged_data.empty:
            print(f"{file_name} 병합 결과가 비어 있습니다.")
            continue
        
        # anomaly 값에 따라 F1 컬럼 생성 ('-1'이면 'AN', '1'이면 'N')
        merged_data['F1'] = merged_data['F1'].apply(lambda x: 'AN' if x == -1 else 'N')
        
        # F1과 grid_label만 남기기
        final_data = merged_data[['F1', 'grid_label']]
        
        # 결과 파일 저장
        output_file_path = os.path.join(output_folder, f'{file_name}')
        final_data.to_csv(output_file_path, index=False)
        
        print(f"{output_file_path} 파일이 저장되었습니다.")
