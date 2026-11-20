# -*- coding: utf-8 -*-
"""Обложка соцсетей и иконки в едином стиле. Требует Pillow; запускать отдельно."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[2]
FONT=Path('/System/Library/Fonts/Supplemental')
def font(size,bold=False):return ImageFont.truetype(str(FONT/('Arial Bold.ttf' if bold else 'Arial.ttf')),size)
BG='#faf9f6';INK='#161b14';ACCENT='#536139';MUTED='#596151'
def mark(d,x,y,h):
    w=h*.38
    d.polygon([(x+h*.4,y),(x+h*.4+w,y),(x+w,y+h),(x,y+h)],fill=ACCENT)
im=Image.new('RGB',(1200,630),BG);d=ImageDraw.Draw(im)
mark(d,64,53,40);d.text((103,49),'IT Компания',font=font(36,True),fill=INK)
d.line([(64,122),(1136,122)],fill='#d5d9cc',width=2)
for y,text in [(174,'Сайты и приложения'),(261,'для вашего бизнеса')]:d.text((64,y),text,font=font(68,True),fill=INK)
d.text((66,376),'Разработка · Дизайн · Автоматизация',font=font(29),fill=MUTED)
d.rounded_rectangle((64,465,1136,559),radius=12,fill='#e8ebdf')
d.text((89,493),'Сайты от 30 000 руб.  ·  Магазины от 50 000 руб.',font=font(28,True),fill=ACCENT)
d.text((65,587),'itcompania.ru',font=font(20),fill=MUTED)
im.save(ROOT/'og-image.png',optimize=True)
for name,size in [('logo.png',512),('apple-touch-icon.png',180)]:
    im=Image.new('RGB',(size,size),BG);d=ImageDraw.Draw(im);mark(d,size*.17,size*.23,size*.25)
    d.text((size*.44,size*.2),'IT',font=font(int(size*.25),True),fill=INK)
    d.text((size*.11,size*.59),'Компания',font=font(int(size*.145),True),fill=ACCENT)
    im.save(ROOT/name,optimize=True)
im.resize((64,64)).save(ROOT/'favicon.ico',sizes=[(16,16),(32,32),(64,64)])
print('Updated OG image, logo and icons')
