import os
from pypdf import PdfWriter

INPUT_DIR = "./output"

merger = PdfWriter()
directory = os.fsencode(INPUT_DIR)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    merger.append(INPUT_DIR + "/" + filename)

merger.write("result.pdf")
merger.close()
print("Done")