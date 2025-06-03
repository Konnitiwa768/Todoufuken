from PIL import Image
import numpy as np
import csv

# === 設定 ===
input_path = 'chaos/map/default.png'
output_path = 'chaos/map/provinces.png'
definition_csv_path = 'chaos/map/definition.csv'
MAX_PROVINCES = 13375

DEFAULT_TYPE = 'land'
DEFAULT_CONTINENT = '1'

# === 色生成（規則的に13375色を用意） ===
def generate_color_list(max_colors):
    colors = []
    step = max(1, int(256 ** 3 / (max_colors + 1)))
    for i in range(1, max_colors + 1):
        val = i * step
        r = (val >> 16) & 0xFF
        g = (val >> 8) & 0xFF
        b = val & 0xFF
        if (r, g, b) != (0, 0, 0):  # 黒は除く
            colors.append((r, g, b))
        else:
            colors.append((r, g, (b + 1) % 255))  # 念のため黒回避
    return colors

unique_colors = generate_color_list(MAX_PROVINCES)

# === 入力画像読み込み ===
image = Image.open(input_path).convert('RGB')
pixels = np.array(image)
height, width = pixels.shape[:2]

output_image = Image.new('RGB', (width, height))

# === プロヴィンス割り当て ===
input_color_to_province_id = {}
province_id_to_color = {}
definitions = []

province_id = 1

for y in range(height):
    for x in range(width):
        orig_color = tuple(pixels[y][x])
        if orig_color == (0, 0, 0):
            output_image.putpixel((x, y), (0, 0, 0))  # 無効地形は黒のまま
            continue
        if orig_color not in input_color_to_province_id:
            if province_id > MAX_PROVINCES:
                raise Exception("プロヴィンス数が上限（13375）を超えました")
            assigned_color = unique_colors[province_id - 1]
            input_color_to_province_id[orig_color] = province_id
            province_id_to_color[province_id] = assigned_color
            definitions.append([
                province_id, DEFAULT_TYPE,
                *assigned_color, DEFAULT_CONTINENT,
                f'province_{province_id}'
            ])
            province_id += 1
        pid = input_color_to_province_id[orig_color]
        output_image.putpixel((x, y), province_id_to_color[pid])

# === 出力 ===
output_image.save(output_path)
with open(definition_csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    for row in definitions:
        writer.writerow(row)

print(f'✅ 完了: {province_id - 1} プロヴィンス塗り分け済')
print(f'🖼️ 保存: {output_path}')
print(f'📄 定義CSV: {definition_csv_path}')
