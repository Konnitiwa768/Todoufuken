from PIL import Image
import numpy as np
import csv
import os

# 入力と出力ファイルパス
input_path = 'chaos/map/default.png'
output_png_path = 'chaos/map/provinces.png'
definition_csv_path = 'chaos/map/definition.csv'

# 最大プロヴィンス数
MAX_PROVINCES = 13375

# プロヴィンスタイプ（仮にすべて land）
DEFAULT_TYPE = 'land'
DEFAULT_CONTINENT = '1'  # 仮設定

# PNG画像を開く
image = Image.open(input_path).convert('RGB')
pixels = np.array(image)

# 色ごとの辞書（RGBタプル → province ID）
color_to_id = {}
id_to_color = {}

province_id = 1  # 0は無効として、1から開始

# 結果画像を初期化（同じサイズ）
output_image = Image.new('RGB', image.size)

# 定義ファイル用リスト
definitions = []

# 画像サイズ取得
height, width = pixels.shape[:2]

# 全ピクセルをスキャンして色を割り当て
for y in range(height):
    for x in range(width):
        color = tuple(pixels[y][x])
        if color == (0, 0, 0):
            continue  # 黒はスキップ（無効エリア）
        if color not in color_to_id:
            if province_id > MAX_PROVINCES:
                raise ValueError("プロヴィンス数が上限（13375）を超えました。")
            color_to_id[color] = province_id
            id_to_color[province_id] = color
            definitions.append([province_id, DEFAULT_TYPE, *color, DEFAULT_CONTINENT, f'province_{province_id}'])
            province_id += 1
        # 出力画像にも同じ色で反映
        output_image.putpixel((x, y), color)

# provinces.png を保存
output_image.save(output_png_path)

# definition.csv を保存
with open(definition_csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    for row in definitions:
        writer.writerow(row)

print(f'プロヴィンス数: {province_id - 1}')
print(f'PNG出力完了: {output_png_path}')
print(f'Definition出力完了: {definition_csv_path}')
