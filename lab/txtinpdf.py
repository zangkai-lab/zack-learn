from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import uuid
import os

def generate_random_number():
    return str(uuid.uuid4())[:8]

def add_text_to_pdf(input_pdf, output_pdf, text):
    # 读取输入的PDF文件
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # 获取第一页
    page = reader.pages[0]

    # 创建一个新的PDF,包含我们要添加的文本
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 12)
    can.drawString(10, 10, text)  # 在(50, 750)位置添加文本
    can.save()

    # 移动到开始位置并读取新创建的PDF
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # 将新PDF合并到现有页面
    page.merge_page(new_pdf.pages[0])

    # 添加修改后的页面
    writer.add_page(page)

    # 写入输出文件
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)


def process_pdfs(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(1, 9):
        input_pdf = os.path.join(input_dir, f"case{i}.pdf")
        output_pdf = os.path.join(output_dir, f"case{i}_labeled.pdf")
        
        if os.path.exists(input_pdf):
            random_number = generate_random_number()
            header_text = f"PDF-Number: EM-{random_number}"
            
            add_text_to_pdf(input_pdf, output_pdf, header_text)
            print(f"已处理 case{i}.pdf，添加标签 {header_text}")
        else:
            print(f"未找到 case{i}.pdf")
# 使用示例
input_pdf = "/Users/zack/Desktop/tools/test/pdf-test"
output_pdf = "/Users/zack/Desktop/tools/test/pdf-test/output"

process_pdfs(input_pdf, output_pdf)
print("所有PDF处理完成。")