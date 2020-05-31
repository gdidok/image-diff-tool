
import csv
import sys
import math, operator
import time
import uuid
from PIL import Image, ImageChops
from functools import reduce

# Rounds the root value to two decimal points and casts to int if 0.0
def roundToTwoDecimal(number):
    rounded = round(number / 100, 2)
    if rounded == 0.0:
        rounded = int(rounded)
    return rounded

# Compare image histograms and return root-mean-square (RMS) value
def compareImages(imgPath1, imgPath2):
    img1 = Image.open(imgPath1)
    img2 = Image.open(imgPath2)
    
    # Try comparing images. If images are diferent return 1
    try:
        h = ImageChops.difference(img1, img2).histogram()
    except ValueError:
        return 1

    # Calculate square ()
    square = reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256)))
    # Calculate Mean  
    mean = (square / (float(img1.size[0]) * img1.size[1]))
    # Calculate Root 
    root = math.sqrt(mean)
    # Round or cast to int
    rounded = roundToTwoDecimal(root)
    return rounded

# Read provided CSV and generate new CSV with scored images
def main(csvFilePath):
    result = []
    # Define columns for result table
    resultCols = ['image1', 'image2', 'similar', 'elapsed']

    with open(csvFilePath, 'r') as csvFile:
        reader = csv.reader(csvFile)
        next(reader)
        for row in reader:
            imgPath1 = row[0]
            imgPath2 = row[1]
            # Calc RMS value (Score) and measure time taken by operation
            start = time.time()
            rms = compareImages(imgPath1, imgPath2)
            end = time.time()
            # Get time elapsed
            elapsed = round(end - start, 3)
            # Add new entry to result arr
            result.append({resultCols[0]: imgPath1, resultCols[1]: imgPath2, resultCols[2]: rms, resultCols[3]: elapsed})

    # Generate a unique filename using UUID
    newFileName = 'scored-images-' + str(uuid.uuid1()).split('-',1)[0] + '.csv'
    # Write the generated arr to a new CSV file
    with open(newFileName, 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=resultCols)
        writer.writeheader()
        for data in result:
            writer.writerow(data)

# Get CSV file path from second arg of CLI
filePath = sys.argv[1]
# Main method
main(filePath)