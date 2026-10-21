from pathlib import Path
from pypdf import PdfReader, PdfWriter


def get_pdf_path(prompt):
    """Ask for a PDF file path and validate it."""
    while True:
        file_path = Path(input(prompt).strip().strip('"')).expanduser()

        if not file_path.is_file():
            print("Error: File not found. Please enter a valid path.")
            continue

        if file_path.suffix.lower() != ".pdf":
            print("Error: Please select a PDF file.")
            continue

        try:
            reader = PdfReader(str(file_path))

            if reader.is_encrypted:
                print("Error: Encrypted PDFs are not supported.")
                continue

            return file_path

        except Exception as error:
            print(f"Error: Unable to read this PDF: {error}")


def get_output_path(prompt):
    """Ask for an output path and validate it."""
    while True:
        output_path = Path(input(prompt).strip().strip('"')).expanduser()

        if output_path.suffix.lower() != ".pdf":
            output_path = output_path.with_suffix(".pdf")

        if output_path.exists():
            overwrite = input(
                "This file already exists. Overwrite it? (y/n): "
            ).strip().lower()

            if overwrite != "y":
                continue

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            return output_path

        except OSError as error:
            print(f"Error creating output directory: {error}")


def merge_pdfs():
    """Merge multiple PDF files into one PDF."""
    print("\n--- Merge PDF Files ---")
    print("Enter the paths of PDF files one by one.")
    print("Type 'done' when you have entered all files.")

    pdf_files = []

    while True:
        file_path = input(
            f"Enter PDF path ({len(pdf_files) + 1}) or 'done': "
        ).strip().strip('"')

        if file_path.lower() == "done":
            break

        if not file_path:
            print("Please enter a path.")
            continue

        path = Path(file_path).expanduser()

        if not path.is_file() or path.suffix.lower() != ".pdf":
            print("Error: Please enter a valid PDF file path.")
            continue

        try:
            reader = PdfReader(str(path))

            if reader.is_encrypted:
                print("Error: Encrypted PDFs are not supported.")
                continue

            # Check that the PDF can be read.
            len(reader.pages)
            pdf_files.append(path)
            print(f"Added: {path.name}")

        except Exception as error:
            print(f"Unable to read PDF: {error}")

    if len(pdf_files) < 2:
        print("Please select at least two valid PDF files to merge.")
        return

    output_path = get_output_path("Enter output PDF path: ")

    try:
        writer = PdfWriter()

        for pdf_file in pdf_files:
            writer.append(str(pdf_file))

        with output_path.open("wb") as output_file:
            writer.write(output_file)

        print(f"\nSuccess! Merged PDF saved to:\n{output_path}")

    except Exception as error:
        print(f"Error merging PDFs: {error}")

    finally:
        if "writer" in locals():
            writer.close()


def split_pdf():
    """Split a PDF into separate one-page PDF files."""
    print("\n--- Split PDF ---")

    pdf_path = get_pdf_path("Enter the PDF path: ")

    try:
        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)

        if total_pages < 2:
            print("This PDF contains fewer than two pages.")
            return

        print(f"Total pages: {total_pages}")

        output_directory = Path(
            input("Enter output directory: ").strip().strip('"')
        ).expanduser()

        output_directory.mkdir(parents=True, exist_ok=True)

        for page_number in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_number])

            output_path = output_directory / (
                f"{pdf_path.stem}_page_{page_number + 1}.pdf"
            )

            with output_path.open("wb") as output_file:
                writer.write(output_file)

            writer.close()
            print(f"Created: {output_path.name}")

        print(f"\nSuccess! All pages saved in:\n{output_directory}")

    except Exception as error:
        print(f"Error splitting PDF: {error}")


def parse_page_range(page_input, total_pages):
    """Convert page numbers and ranges into zero-based page indexes."""
    selected_pages = set()

    for part in page_input.split(","):
        part = part.strip()

        if not part:
            raise ValueError("Empty page selection.")

        if "-" in part:
            if part.count("-") != 1:
                raise ValueError(f"Invalid page range: {part}")

            start_text, end_text = part.split("-")
            start = int(start_text.strip())
            end = int(end_text.strip())

            if start < 1 or end < start or end > total_pages:
                raise ValueError(f"Invalid page range: {part}")

            selected_pages.update(range(start - 1, end))

        else:
            page = int(part)

            if page < 1 or page > total_pages:
                raise ValueError(f"Invalid page number: {page}")

            selected_pages.add(page - 1)

    if not selected_pages:
        raise ValueError("Select at least one page.")

    return sorted(selected_pages)


def extract_pages():
    """Extract selected pages into a new PDF."""
    print("\n--- Extract Specific Pages ---")

    pdf_path = get_pdf_path("Enter the PDF path: ")

    try:
        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)

        print(f"Total pages: {total_pages}")
        print("Examples: 1,3,5 or 2-5 or 1,3-5,8")

        while True:
            page_input = input(
                "Enter page numbers or ranges: "
            ).strip()

            try:
                selected_pages = parse_page_range(
                    page_input, total_pages
                )
                break

            except ValueError as error:
                print(f"Invalid selection: {error}")
                print("Please try again.")

        output_path = get_output_path("Enter output PDF path: ")

        # Avoid accidentally overwriting the source PDF.
        if output_path.resolve() == pdf_path.resolve():
            print("Error: Output path must differ from the source PDF.")
            return

        writer = PdfWriter()

        for page_index in selected_pages:
            writer.add_page(reader.pages[page_index])

        try:
            with output_path.open("wb") as output_file:
                writer.write(output_file)
        finally:
            writer.close()

        print(f"\nSuccess! Extracted {len(selected_pages)} page(s).")
        print(f"Saved to: {output_path}")

    except Exception as error:
        print(f"Error extracting pages: {error}")


def display_menu():
    """Display the application's main menu."""
    print("\n" + "=" * 38)
    print("       PDF MERGER & SPLITTER")
    print("=" * 38)
    print("1. Merge PDF files")
    print("2. Split PDF into separate pages")
    print("3. Extract specific pages")
    print("4. Exit")
    print("=" * 38)


def main():
    """Run the PDF Merger & Splitter application."""
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            merge_pdfs()
        elif choice == "2":
            split_pdf()
        elif choice == "3":
            extract_pages()
        elif choice == "4":
            print("Thank you for using PDF Merger & Splitter!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()