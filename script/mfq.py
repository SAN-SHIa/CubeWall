from PIL import Image

# 加载原始图片
image_path = 'source.jpg' 
image = Image.open(image_path)

# 从图片中选择6种颜色
target_colors = [(10, 10, 36),  # 蓝色
                 (186, 135, 132),  # 白色
                 (89, 35, 35),  # 红色
                 (174, 122, 124),  # 橙色
                 (170, 163, 93),  # 黄色
                 (59, 103, 42)]  # 绿色

# 缩放图片到75x75像素
image_resized = image.resize((75, 75), Image.Resampling.LANCZOS)

# 创建一个新图片，用于存放量化后的颜色
quantized_image = Image.new('RGB', (75, 75))
expand_image = Image.new('RGB', (1000, 1000))


# 一个魔方块8*8像素
width, height = 8, 8

transform={
    (10, 10, 36): (8,170,255),  # 蓝色
    (186, 135, 132): (254,251,246), # 白色
    (89, 35, 35): (252,55,38),   # 红色
    (174, 122, 124): (255,172,80), # 橙色
    (170, 163, 93):(255,255,115),# 黄色
    (59, 103, 42): (128,251,137) # 绿色
}


# 量化过程：将每个像素映射到最接近的目标颜色
for x in range(image_resized.width):
    for y in range(image_resized.height):
        pixel = image_resized.getpixel((x, y))
        # 使用欧几里得距离找到最近的匹配颜色
        closest_color = min(target_colors, key=lambda color: sum((c - p) ** 2 for c, p in zip(color, pixel)))
        quantized_image.putpixel((x, y), closest_color)
        for i in range(8):
            for j in range(8):
                expand_image.putpixel((x*12+i,y*12+j),transform[closest_color])

# 扩展图片900*900像素 成25*25的小块
blocks = []
for i in range(25):
    for j in range(25):
        block = expand_image.crop((j * 36, i * 36, (j + 1) * 36, (i + 1) * 36))
        blocks.append(block)


# 创建一个1000x1000像素的新图片作为魔方墙
wall = Image.new('RGB', (994, 994))

# 将小块按照魔方布局排列
for i, block in enumerate(blocks):
    x = (i % 25) * 40
    y = (i // 25) * 40
    wall.paste(block, (x, y))

# 保存量化后的魔方墙图片
wall.save('output.bmp')
wall.show()
# expand_image.save('expand.bmp')
# expand_image.show()