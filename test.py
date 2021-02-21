import PyPDF2
import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


pdfFileObject = open('I:\\data_set_download\\gg.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
count = pdfReader.numPages
for i in range(count):
    page = pdfReader.getPage(i)
    s = str(page.extractText())

print(s)
dictionary.index('ABSTRACT')
