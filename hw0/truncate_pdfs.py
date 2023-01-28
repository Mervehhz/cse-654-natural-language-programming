import fitz
import re
from os import listdir

pdfs = listdir("pdfs")
doc_num = 1
LINE_NUM = 400

for pdf in pdfs:
    with fitz.open(f"pdfs/{pdf}") as doc:
        text = ""
        for i in range(11, doc.page_count-10):
            text += doc.load_page(i).get_text()

    for m in re.finditer("([A-Za-zÜüĞğŞşİiIıÖöÇç]+-\n[a-züğşiıöç]+)", text):
        text = text.replace(m.group(), m.group().replace("-\n", "")+"\n")

    text = re.sub("(\.+\n)", "", text)
    text = re.sub("(\d+\n)", "", text)
    text = re.sub("(\w\n)", "", text)

    lines = text.splitlines()
    truncated_text = ""
    for i in range(1, len(lines)):
        truncated_text += lines[i] + "\n"
        if i % LINE_NUM == 0 or i == len(lines)-1:
            with open(f"txts/{doc_num}.txt", "w+", encoding="utf-8") as f:
                f.write(truncated_text)
            doc_num += 1
            truncated_text = ""
