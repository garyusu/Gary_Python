from docx import Document
from docx.shared import Pt, Cm #處理大小，字體或空間
import os

document = Document()
section = document.sections[0]
section.left_margin = Cm(1.27)
section.right_margin = Cm(1.27)
section.top_margin = Cm(1.27)
section.bottom_margin = Cm(1.27)
print(section)
document.save("tmp.docx")

# os.remove("tmpPic.jpg")