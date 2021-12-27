#!/usr/bin/env fades

import datetime
import os
import subprocess

import cv2  # fades opencv-python
import numpy as np  # fades

TMP_SCAN = "temp-scan-file.pnm"


def extract_images(imagepath_prefix):
    """Extract the photos from the big scan."""
    print("    extracting images")
    image = cv2.imread(TMP_SCAN)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

    thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    threshold_area = 500_000
    image_idx = 1
    for c in cnts:
        area = cv2.contourArea(c)
        if area > threshold_area:
            # really a photo!
            x, y, w, h = cv2.boundingRect(c)
            ROI = image[y:y + h, x:x + w]
            imagepath = imagepath_prefix + f"{image_idx}.jpeg"
            print(f"    saving image {imagepath} ({w}x{h})")
            cv2.imwrite(imagepath, ROI)
            image_idx += 1


def scan():
    cmd = [
        "scanimage",
        "--source", "Flatbed",
        "--mode", "Color",
        "--resolution", "300",
        "--format=pnm",
        "--output-file", TMP_SCAN,
    ]
    while True:
        print("    scanning...")
        proc = subprocess.run(cmd)
        if proc.returncode:
            print(f"        bad return code: {proc.returncode}")
            continue
        if os.stat(TMP_SCAN).st_size == 0:
            print("        empty output file")
            continue
        break


while True:
    while True:
        choice = input(
            "\nPut photos in the scanner and choose: [P] photos (default), [R] raw scan:")
        choice = choice.strip().lower()
        if choice in ("", "p", "r"):
            break

    now = datetime.datetime.now()
    imagepath_prefix = f"photo-{now:%Y%m%d-%H%M%S}-"
    if choice == "r":
        # get a raw scan and just rename it
        scan()
        imagepath = imagepath_prefix + "X.pnm"
        os.rename(TMP_SCAN, imagepath)
        print("    raw saved as", imagepath)
    else:
        # get a raw scan and extract the images from it
        scan()
        extract_images(imagepath_prefix)
        os.unlink(TMP_SCAN)
