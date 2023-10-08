from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont

font_path = '../fonts/KGNeatlyPrinted.ttf'
font_name = 'KGNeatlyPrinted'
font = TTFont(font_name, font_path)
registerFont(font)

title_font_path = '../fonts/ArchitectsDaughter.ttf'
title_font_name = 'ArchitectsDaughter'
title_font = TTFont(title_font_name, title_font_path)
registerFont(title_font)


__all__ = ["pdf_client"]