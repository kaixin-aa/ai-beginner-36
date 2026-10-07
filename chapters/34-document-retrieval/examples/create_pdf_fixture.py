"""原创两页文字PDF与仅图片错误样例，固定内容不使用真人资料。"""
from io import BytesIO
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
PAGES=[['柳叶学习室设备借用说明','本文为原创虚构教学资料，不对应真实机构。','柳叶学习室投影仪一次最长借用90分钟。','设备编号P01，仅限室内使用。'],
       ['设备归还规则','本文为原创虚构教学资料，不对应真实机构。','柳叶学习室投影仪使用结束后，先关闭电源，再归还到服务台。','管理员核对设备编号并登记归还时间。']]

def create():
    target=ROOT/'data/documents';target.mkdir(parents=True,exist_ok=True)
    font_path=Path('C:/Windows/Fonts/msyh.ttc')
    pdfmetrics.registerFont(TTFont('FixtureChinese',str(font_path),subfontIndex=0))
    pdf=canvas.Canvas(str(target/'equipment.pdf'),pagesize=(595,842),invariant=1)
    pdf.setTitle('柳叶学习室原创教学设备规则')
    for number,lines in enumerate(PAGES,1):
        pdf.setFillColorRGB(.12,.22,.34);pdf.setFont('FixtureChinese',20);pdf.drawString(55,765,lines[0])
        pdf.setFont('FixtureChinese',12)
        for i,line in enumerate(lines[1:]):pdf.drawString(55,700-i*44,line)
        pdf.setFillColorRGB(.4,.45,.5);pdf.drawString(55,65,f'原创教学资料   第{number}页，共2页')
        pdf.showPage()
    pdf.save()
    invalid=ROOT/'data/invalid';invalid.mkdir(exist_ok=True)
    image=Image.new('RGB',(900,220),'white');draw=ImageDraw.Draw(image)
    draw.text((30,65),'仅图片的扫描教学样例',font=ImageFont.truetype(str(font_path),40),fill='black')
    scan=canvas.Canvas(str(invalid/'image-only.pdf'),pagesize=(595,842),invariant=1)
    scan.drawImage(ImageReader(image),45,600,width=500,height=122);scan.save()
    print('已生成2页文字PDF及1页图片PDF错误样例')

if __name__=='__main__':create()
