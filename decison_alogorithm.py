import grid
import os
import pandas as pd
import path_db

class User_Path:
    def __init__(self):
        #사용자 그리드 생성을 위한 경로 데이터 가져오기
        file=pd.read_csv(os.getcwd()+'/IF/anomaly_score.csv')
        path_points = file[['lat', 'lng']].values.tolist()
        self.user_path=[]

        #grid.py의 GridProcessor 클래스 사용
        gd=grid.GridProcessor()
        grid_queue = gd.generate_initial_grids()
        self.final_grids = gd.subdivide_grids(grid_queue, path_points)

    #그리드가 중복되었는지 확인
    def accum_checker(self, grid):
        if self.user_path[-1]!=grid:
            return self.user_path.append(grid)
        else:
            return self.user_path

    #위도, 경도가 들어왔을 때 N/AN 인지 확인하고 리턴하는 함수
    def decision(self, lat, lng):
        label=grid.GridProcessor.get_grid_label(lat, lng, self.final_grids)
        
        #누적된 경로 구하기
        accum_path=self.accum_check(label)
        result=self.db_path_checker(accum_path)
        
        #N/AN 인지 리턴
        return result

    def db_path_checker(self, accum_path):
        #유저의 경로 데이터 전처리
        path_str=str(accum_path).replace('[', '').replace(']', '').replace(' ', '').replace(',', '').replace("'", "")

        #db와 확인
        path_db.init()
        return path_db.path_checker(path_str)
        