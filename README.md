# 📄 PDF Merger & Splitter

A Python application that makes working with PDF files simple. Merge multiple PDF documents into one file, split PDFs into separate documents, and extract specific pages using an easy-to-use, menu-driven interface.

## ✨ Features

- 📎 **Merge PDFs:** Combine multiple PDF files into a single document.
- ✂️ **Split PDFs:** Split a PDF into separate files, one page per file.
- 📑 **Extract Pages:** Extract specific pages or a selected page range.
- 🔢 **Page Selection:** Specify which pages to extract.
- 🛡️ **Input Validation:** Validate file paths and page numbers.
- ⚠️ **Error Handling:** Handle missing files, invalid page ranges, and PDF processing errors.
- 💻 **Simple Interface:** Use a straightforward command-line menu.
- 🔒 **Original File Protection:** Keep the original PDF files unchanged.

## 🛠️ Technologies Used

- Python 3
- pypdf
- File Handling
- Exception Handling

## 📂 Project Structure

```text
pdf-merger-splitter/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or later
- pip (Python package installer)

### 1. Clone the Repository

```bash
git clone https://github.com/Shivamtripathi78/pdf-merger-splitter.git
```

### 2. Navigate to the Project Directory

```bash
cd pdf-merger-splitter
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

## 📖 How to Use

After starting the application, select an operation from the menu.

### Merge PDFs
1. Select the merge option.
2. Enter the paths of the PDF files you want to combine.
3. Specify the output file path.
4. The application creates a single PDF containing the selected documents.

### Split a PDF
1. Select the split option.
2. Enter the source PDF path.
3. Specify the output directory.
4. The application saves each page as a separate PDF file.

### Extract Specific Pages
1. Select the page extraction option.
2. Enter the source PDF path.
3. Specify the page numbers or page range.
4. Enter the output file path.
5. The selected pages are saved into a new PDF.

*The exact menu options and input format depend on the implementation in `main.py`.*

## 👨‍💻 Author

**Shivam Tripathi**

- GitHub: [@Shivamtripathi78](https://github.com/Shivamtripathi78)
