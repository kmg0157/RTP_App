import pandas as pd
import string
import os
import geopy.distance
import folium

class GridProcessor:
    def __init__(self):
        """
        초기화 함수
        :param bounds: 지역 경계 (남쪽, 서쪽, 북쪽, 동쪽)
        :param min_size_km: 최소 그리드 크기 (km)
        :param grid_size: 초기 그리드 크기 (분할 수)
        """
        self.bounds = [33.10, 124.57, 38.60, 131]
        self.min_size_km = 0.76
        self.grid_size = 13

    @staticmethod
    def num_to_letter(num):
        """숫자를 문자로 변환"""
        return string.ascii_uppercase[num]

    def generate_initial_grids(self):
        """초기 그리드 생성"""
        south, west, north, east = self.bounds
        lat_step = (north - south) / self.grid_size
        lon_step = (east - west) / self.grid_size
        grid_queue = []

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                grid_south = south + i * lat_step
                grid_north = south + (i + 1) * lat_step
                grid_west = west + j * lon_step
                grid_east = west + (j + 1) * lon_step
                grid_queue.append((grid_south, grid_west, grid_north, grid_east, 
                                   self.num_to_letter(i) + self.num_to_letter(j)))

        return grid_queue

    @staticmethod
    def is_path_in_grid(south, west, north, east, path_points):
        """경로가 그리드 안에 있는지 확인"""
        return any(south <= lat <= north and west <= lng <= east for lat, lng in path_points)

    def subdivide_grids(self, grid_queue, path_points):
        """그리드 분할"""
        final_grids = []

        while grid_queue:
            south, west, north, east, grid_label = grid_queue.pop(0)
            grid_size_km = min(geopy.distance.distance((south, west), (south, east)).km,
                               geopy.distance.distance((south, west), (north, west)).km)
            
            if grid_size_km > self.min_size_km and self.is_path_in_grid(south, west, north, east, path_points):
                mid_lat = (south + north) / 2
                mid_lon = (west + east) / 2
                grid_queue.append((south, west, mid_lat, mid_lon, grid_label + 'C'))
                grid_queue.append((mid_lat, west, north, mid_lon, grid_label + 'A'))
                grid_queue.append((south, mid_lon, mid_lat, east, grid_label + 'D'))
                grid_queue.append((mid_lat, mid_lon, north, east, grid_label + 'B'))
            else:
                final_grids.append((south, west, north, east, grid_label))

        return final_grids

    @staticmethod
    def get_grid_label(lat, lng, final_grids):
        """해당 위치의 그리드 레이블 찾기"""
        for south, west, north, east, grid_label in final_grids:
            if south <= lat <= north and west <= lng <= east:
                return grid_label
        return None

    @staticmethod
    def visualize_path_with_grids(data, final_grids, output_html_path, bounds):
        """지도에 경로와 그리드 레이블 시각화"""
        m = folium.Map(location=[(bounds[0] + bounds[2]) / 2, (bounds[1] + bounds[3]) / 2], zoom_start=7)

        points = data[['lat', 'lng']].values.tolist()
        folium.PolyLine(points, color='red', weight=2.5, opacity=1).add_to(m)

        for south, west, north, east, grid_label in final_grids:
            folium.Rectangle(
                bounds=[[south, west], [north, east]],
                color='#0000FF',
                fill=True,
                fill_opacity=0.1
            ).add_to(m)
            folium.Marker(
                location=[(south + north) / 2, (west + east) / 2],
                icon=folium.DivIcon(html=f'<div style="font-size: 8pt; color: yellow;">{grid_label}</div>')
            ).add_to(m)

        m.save(output_html_path)

    def process_file(self, file_path, output_path, output_html_path):
        """단일 파일 처리"""
        data = pd.read_csv(file_path, encoding='utf-8')
        path_points = data[['lat', 'lng']].values.tolist()

        grid_queue = self.generate_initial_grids()
        final_grids = self.subdivide_grids(grid_queue, path_points)

        data['grid_label'] = data.apply(lambda row: self.get_grid_label(row['lat'], row['lng'], final_grids), axis=1)
        data.to_csv(output_path, index=False)

        self.visualize_path_with_grids(data, final_grids, output_html_path, self.bounds)


# 예제
if __name__ == "__main__":
    dataset_path = r"C:\Users\NetDB\Desktop\RTP2\IF\anomaly_score.csv"
    output_file_path = r"C:\Users\NetDB\Desktop\RTP2\IF\anomaly_score_labeled1.csv"
    output_html_path = r"C:\Users\NetDB\Desktop\RTP2\IF\anomaly_score_map1.html"

    grid_processor = GridProcessor()
    grid_processor.process_file(dataset_path, output_file_path, output_html_path)
