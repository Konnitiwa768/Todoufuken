from PIL import Image
import numpy as np
import csv
import os

# 入力と出力ファイルパス
input_path = 'chaos/map/default.png'
output_bmp_path = 'chaos/map/provinces.bmp'
definition_csv_path = 'chaos/map/definition.csv'

# 最大プロヴィンス数
MAX_PROVINCES = 13375

# プロヴィンスのタイプ（land, sea など。ここでは仮にすべてland）
DEFAULT_TYPE = 'land'
DEFAULT_CONTINENT = '1'  # 仮

# PNG画像を開く
image = Image.open(input_path).convert('RGB')
pixels = np.array(image)

# 色ごとの辞書（RGBタプル → province ID）
color_to_id = {}
id_to_color = {}

province_id = 1  # 0は無効なので、1から開始

# 結果画像を初期化（同じサイズ）
output_image = Image.new('RGB', image.size)

# 定義情報格納
definitions = []

# 画像サイズ
height, width = pixels.shape[:2]

# 画素走査とID付与
for y in range(height):
    for x in range(width):
        color = tuple(pixels[y][x])
        if color == (0, 0, 0):
            continue  # 黒はスキップ（海または無効）
        if color not in color_to_id:
            if province_id > MAX_PROVINCES:
                raise ValueError("プロヴィンス数が上限を超えました。")
            color_to_id[color] = province_id
            id_to_color[province_id] = color
            definitions.append([province_id, DEFAULT_TYPE, *color, DEFAULT_CONTINENT, f'province_{province_id}'])
            province_id += 1
        # 書き込み用画像にIDの色を反映
        output_image.putpixel((x, y), color)

# 保存
output_image.save(output_bmp_path)

# definition.csv を保存
with open(definition_csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    for row in definitions:
        writer.writerow(row)

print(f'プロヴィンス数: {province_id - 1}')
print(f'出力完了: {output_bmp_path}, {definition_csv_path}')
