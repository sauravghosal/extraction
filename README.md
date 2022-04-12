# Text Extraction from GhosalRE Cabin Occupancy Reports

A command line tool to extract the text from a GhosalRE occupancy report image. For identifying the locations of the cells in the table, OpenCV is used, and for converting images to text, Google's tesseract OCR engine is used.

## How to use

1.  Install Google Tesseract (platform-dependent)

    ### Steps for Windows

    - Visit [this installation link](https://digi.bib.uni-mannheim.de/tesseract/)
    - Configure installation
    - Add path to tesseract executable to PATH

    ### Steps for Linux (Debian and Ubuntu distros)

    Install using apt

        $ sudo apt install tesseract-ocr -y

    ### Steps for MacOS

    Install using homebrew package manager

        $ brew install tesseract

2.  Install python version 3.8

3.  Install pipenv

        $ pip install --user pipenv

4.  Install dependencies from Pipfile

        $ pipenv install

5.  Activate virtual environment

        $ pipenv shell

6.  Run `extract.py` script with arguments

        $ python extract.py [-h] [-s] inFile columns outFile

| Parameter | Description                                                                 | Required |
| --------- | --------------------------------------------------------------------------- | -------- |
| inFile    | path to the cabin performance report png                                    | Yes      |
| columns   | number of columns in report table                                           | Yes      |
| outFile   | path of excel file to write to                                              | Yes      |
| -h        | (no argument) displays program help text                                    | No       |
| -s        | (no argument) show bounding boxes around extracted text in the report image | No       |
