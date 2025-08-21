import base64
import io
import logging
from PIL import Image, ImageDraw
from typing import List, Tuple, Union, Optional



# 为颜色值创建一个更准确的类型别名，表示它可以是字符串，或RGB元组，或RGBA元组
ColorValue = Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]

def draw_circles_on_image_v2(
    base64_image_string: str,
    coordinates: List[Tuple[int, int]],
    radius: int = 15,
    # 修正后的类型提示：可以是 ColorValue 类型，也可以是 None
    fill_color: Optional[ColorValue] = "red",
    # 修正后的类型提示：可以是 ColorValue 类型
    outline_color: ColorValue = "red",
    outline_width: int = 1
) -> str:
    """
    在一个 base64 编码的图片上根据指定的坐标列表绘制圆形 (版本2)。
    支持自定义填充色、轮廓色和轮廓宽度。
    :param base64_image_string: 图片的 base64 编码字符串。
    :param coordinates: 一个包含(x, y)坐标元组的列表，用于指定圆心位置。
    :param radius: 要绘制的圆的半径，默认为 15 像素。
    :param fill_color: 圆的填充颜色。可以是字符串(如 'red')或元组(如 (255,0,0))。如果为 None，则圆是透明的。
    :param outline_color: 圆的轮廓颜色。
    :param outline_width: 圆的轮廓宽度。
    :return: 经过修改后的图片的 base64 编码字符串。
    """
    try:
        image_data = base64.b64decode(base64_image_string)
        image = Image.open(io.BytesIO(image_data))

        # 转换为 RGBA 模式以支持透明填充
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        draw = ImageDraw.Draw(image)

        for x, y in coordinates:
            bounding_box = [
                (x - radius, y - radius),
                (x + radius, y + radius)
            ]
            draw.ellipse(
                xy=bounding_box,
                fill=fill_color,
                outline=outline_color,
                width=outline_width
            )

        output_buffer = io.BytesIO()
        # 保存为 PNG 格式以保留透明度
        image_format = 'PNG'
        image.save(output_buffer, format=image_format)
        
        byte_data = output_buffer.getvalue()
        new_base64_string = base64.b64encode(byte_data).decode('utf-8')

        return new_base64_string

    except Exception as e:
        print(f"处理图片时发生错误: {e}")
        raise


# --- 使用示例 ---
if __name__ == '__main__':
    # 创建一个用于测试的空白图片
    dummy_image = Image.new('RGB', (400, 400), '#EEEEEE')
    buffered = io.BytesIO()
    dummy_image.save(buffered, format="PNG")
    base64_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # 定义坐标点
    points = [(100, 100), (300, 200)]

    # 调用新函数，画一个半透明的蓝色圆，带粗的黑色轮廓
    modified_base64 = draw_circles_on_image_v2(
        base64_image_string=base64_str,
        coordinates=points,
        radius=50,
        fill_color=(0, 255, 0, 128),  # RGBA 颜色，A=128表示半透明
        outline_color="black",
        outline_width=5
    )

    # 保存结果
    if modified_base64:
        img_data = base64.b64decode(modified_base64)
        output_filename = "output_image_v2.png"
        with open(output_filename, "wb") as f:
            f.write(img_data)
        print(f"图片处理完成，已保存为 '{output_filename}'")
