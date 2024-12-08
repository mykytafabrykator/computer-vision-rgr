import cv2
from pyzbar.pyzbar import decode
import numpy as np
import os


def preprocess_image(image):
    """Попередня обробка для покращення виявлення кодів."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Підвищення контрасту
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Бінаризація
    _, binary = cv2.threshold(
        enhanced, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    return binary


def detect_barcodes_and_qrcodes(image):
    """Виявлення штрихкодів і QR-кодів."""
    detected_items = decode(image)
    results = []

    for item in detected_items:
        data = item.data.decode('utf-8')
        type_of_code = item.type
        rect = item.rect

        results.append({'data': data, 'type': type_of_code, 'rect': rect})

        # Візуалізація коду
        x, y, w, h = rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f"{type_of_code}: {data}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image, results


def process_image(image_path, output_path):
    """Основний процес обробки зображення."""
    image = cv2.imread(image_path)

    binary_image = preprocess_image(image)

    processed_image, results = detect_barcodes_and_qrcodes(image)

    # Поєднання зображень
    binary_colored = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
    combined_image = np.hstack(
        (binary_colored, processed_image)
    )

    cv2.imwrite(output_path, combined_image)

    return results


if __name__ == '__main__':
    file_name = "barcode.png"
    image_path = f"images/{file_name}"
    output_path = f"results/{file_name}"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    results = process_image(image_path, output_path)

    if results:
        print("Розпізнані коди:")
        for result in results:
            print(f"Тип: {result['type']},"
                  f"Дані: {result['data']},"
                  f"Розташування: {result['rect']}"
                  )
        print(f"Об'єднане зображення збережено у файлі: {output_path}")
    else:
        print("Жодних кодів не знайдено.")
