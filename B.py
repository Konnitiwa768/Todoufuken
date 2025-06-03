from PIL import Image
import numpy as np
import csv
import os
import random

# === 入出力パス ===
input_path = 'chaos/map/default.png'
output_path = 'chaos/map/provinces.png'
definition_csv_path = 'chaos/map/definition.csv'

MAX_PROVINCES = 13375

# === プロヴィンス情報 ===
DEFAULT_TYPE = 'land'
DEFAULT_CONTINENT = '1'

# === 使用済みユニーク色管理 ===
used_colors = set()

def generate_unique_color():
    """未使用のユニークな色を返す"""
    while True:
        color = tuple(random.randint(1, 255) for _ in range(3))  # 0は避ける
        if color not in used_colors:
            used_colors.add(color)
            return color

# === 入力画像を読み込む ===
image = Image.open(input_path).convert('RGB')
pixels = np.array(image)
height, width = pixels.shape[:2]

# === 色分類とマッピング処理 ===
input_to_unique = {}   # 入力色 → 出力ユニーク色
definitions = []
output_image = Image.new('RGB', (width, height))

province_id = 1

for y in range(height):
    for x in range(width):
        orig_color = tuple(pixels[y][x])
        if orig_color == (0, 0, 0):
            # 黒は無効色として扱う（そのまま残す）
            output_image.putpixel((x, y), (0, 0, 0))
            continue
        if orig_color not in input_to_unique:
            if province_id > MAX_PROVINCES:
                raise Exception("プロヴィンス数が上限を超えました。")
            unique_color = generate_unique_color()
            input_to_unique[orig_color] = unique_color
            definitions.append([
                province_id,
                DEFAULT_TYPE,
                *unique_color,
                DEFAULT_CONTINENT,
                f'province_{province_id}'
            ])
            province_id += 1
        # 書き込み
        output_image.putpixel((x, y), input_to_unique[orig_color])

# === 出力処理 ===
output_image.save(output_path)

with open(definition_csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    for row in definitions:
        writer.writerow(row)

print(f'完了: {province_id - 1} 個のプロヴィンスを生成')
print(f'保存: {output_path}, {definition_csv_path}')
