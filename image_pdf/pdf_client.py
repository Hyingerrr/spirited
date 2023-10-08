import os
import tempfile

import numpy as np
import cv2
from PIL import Image
from PyPDF2 import PdfMerger
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from image_pdf import font_name, title_font_name


def add_text_convert(image_path, text, output_filename, page_number,
                     image_size=(1360, 1024)):  # 1174 height after adding white space
    """
    :param image_path: 图片地址
    :type image_path: basestring
    :param text: 要添加到图像上的文本内容
    :type text: basestring
    :param output_filename: 生成的PDF文件的输出路径
    :type output_filename: basestring
    :param page_number: 页码 表示要生成的PDF页码
    :type page_number: int
    :param image_size: 图片大小，默认为(1360, 1024)
    :type image_size: tuple
    :return:
    :rtype:
    """
    width, height = image_size

    # 打开图像并调整大小
    img = cv2.imread(image_path)
    img = cv2.resize(img, image_size)

    # 生成淡化蒙版：仅淡化图像底部的20%
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    mask = cv2.rectangle(mask, (0, 0), (img.shape[1], int(img.shape[0] * 0.95)), 255, cv2.FILLED)
    mask = cv2.GaussianBlur(mask, (99, 99), 0)

    # 将图像转换为RGB格式以确保一致性
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 将图像和蒙版转换为PIL格式
    img_pil = Image.fromarray(img_rgb)
    mask_pil = Image.fromarray(mask)

    # 生成白色图像的PIL格式
    white_img_pil = Image.new('RGB', image_size, color='white')

    # 合并图像、白色图像和蒙版
    blended_img_pil = Image.composite(img_pil, white_img_pil, mask_pil)

    new_image = Image.new('RGB', (width, height + 150), color='white')
    new_image.paste(blended_img_pil, (0, 0))

    # 临时保存修改后的图像
    new_image.save("temp.jpg")

    # 创建与新图像相同大小的PDF文档
    c = canvas.Canvas(output_filename, pagesize=(width, height + 150))

    # 将图像绘制到PDF上
    c.drawImage("temp.jpg", 0, 0)

    # 使用来自样式表的基本段落样式
    style = getSampleStyleSheet()['BodyText']
    style.alignment = 1
    style.fontName = font_name
    style.fontSize = 42

    # 将文本分割成段落并添加到PDF中
    text_list = split_paragraph(text, 80)
    for i, element in enumerate(text_list):
        story = [Paragraph(element, style)]
        frame_x = width * 0.015
        frame_y = (height * 0.07) - (i * 35)

        frame = Frame(frame_x, frame_y, width * 0.97, height * 0.1, id='normal')
        frame.addFromList(story, c)

    # 在右下角添加页码
    c.setFont(font_name, 16)  # 增加字体大小
    c.drawString(width - 80, 50, str(page_number))  # Position higher

    c.save()


def generate_page_title(image_path, text, output_filename, image_size=(1360, 1174)):
    """
    生成标题
    :param image_path: 图像位置
    :type image_path: basestring
    :param text: 要添加到图像上的文本内容
    :type text: basestring
    :param output_filename: 生成的PDF文件的输出路径
    :type output_filename: basestring
    :param image_size: 图像大小
    :type image_size: tuple
    :return:
    :rtype:
    """
    img = Image.open(image_path).resize(image_size)
    img.convert('RGB').save("temp.jpg")

    width, height = image_size
    # 创建一个新的PDF文档，与图像大小相匹配
    c = canvas.Canvas(output_filename, pagesize=(width, height))
    # 在PDF文档上绘制图像
    c.drawImage("temp.jpg", 0, 0)

    # 定义文本样式
    style = getSampleStyleSheet()['BodyText']
    style.alignment = 1
    style.fontName = title_font_name
    style.fontSize = 50

    # 计算文本行高和边距
    line_height = style.leading
    padding = 50

    # # 定义白色背景矩形的尺寸和位置
    rect_height = line_height + 2 * padding
    rect_width = width * 0.8  # 使用页面宽度的80%作为矩形宽度
    rect_x = (width - rect_width) / 2  # 居中放置矩形
    rect_y = height - 200  # 设置矩形的位置

    # 绘制白色背景矩形
    c.setFillColor('white')
    c.rect(rect_x, rect_y - rect_height, rect_width, rect_height, fill=1)

    # 为文本的每一行创建一个文本框
    frame_x = rect_x + padding
    frame_y = rect_y - line_height - 100

    frame = Frame(frame_x - 20, frame_y, rect_width - 1 * padding, 100, id='normal', showBoundary=0)
    # 创建包含文本的段落
    story = [Paragraph(text, style)]
    # 将段落添加到文本框中
    frame.addFromList(story, c)

    c.save()


def split_paragraph(paragraph, length):
    words = paragraph.split(' ')
    result = []
    current_length = 0
    current_words = []
    for word in words:
        if current_length + len(word) <= length:
            current_length += len(word) + 1  # +1 for the space
            current_words.append(word)
        else:
            result.append(' '.join(current_words))
            current_words = [word]
            current_length = len(word)
    result.append(' '.join(current_words))  # Add the last words
    return result


def pdf_generator(pages, result_filename) -> str:
    """
    生成PDF
    :param pages: 每页图片地址、描述
    :type pages: list[tuple]
    :param result_filename: 输出pdf地址
    :type result_filename: basestring
    :return: pdf地址
    :rtype: basestring
    """
    pdf_files = []
    images = []

    # 标题
    image_path, text = pages[0]
    images.append(image_path)
    temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    temp_file.close()
    generate_page_title(image_path, text, temp_file.name)
    pdf_files.append(temp_file.name)

    # 内页
    for i, page in enumerate(pages[1:]):
        image_path, text = page
        images.append(image_path)
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_file.close()
        add_text_convert(image_path, text, temp_file.name, page_number=i + 1)

        pdf_files.append(temp_file.name)

    merger = PdfMerger()
    for temp_file in pdf_files:
        merger.append(temp_file)

    merger.write(result_filename)
    merger.close()

    for temp_file in pdf_files:
        os.remove(temp_file)
    os.remove('temp.jpg')
    return result_filename
