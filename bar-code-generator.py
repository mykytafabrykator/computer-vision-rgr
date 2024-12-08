from barcode import EAN13
from barcode.writer import ImageWriter

# Генерація штрихкоду
barcode = EAN13("123456789012", writer=ImageWriter())

# Збереження зображення
barcode.save("/input/barcode")
