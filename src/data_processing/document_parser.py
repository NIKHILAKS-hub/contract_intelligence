import pymupdf
import os


def extract_pdf_text(file_path):

    print("\nOpening PDF:")
    print(file_path)

    # Open PDF
    doc = pymupdf.open(file_path)

    print("Number of pages:", len(doc))

    text = ""

    # Read every page
    for page_number, page in enumerate(doc):

        page_text = page.get_text()

        text += page_text + "\n"

        print(
            f"Page {page_number + 1}: "
            f"{len(page_text)} characters"
        )

    doc.close()

    return text


def clean_text(text):

    # Remove excessive spaces
    text = " ".join(text.split())

    return text


def extract_text(file_path):

    # Check file exists
    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"\nFile not found:\n{file_path}"
        )

    # Check PDF
    if file_path.lower().endswith(".pdf"):

        return extract_pdf_text(file_path)

    else:

        raise ValueError(
            "Currently only PDF files are supported."
        )


def save_text(text, pdf_path):

    # Get PDF filename
    filename = os.path.basename(pdf_path)

    # Remove .pdf
    filename_without_extension = os.path.splitext(
        filename
    )[0]

    # Create output path
    output_path = os.path.join(
        "data",
        "contracts",
        filename_without_extension + ".txt"
    )

    # Save text
    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(text)

    return output_path


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("CONTRACT DOCUMENT PARSER")
    print("=" * 60)

    file_path = input(
        "\nEnter the full path of your PDF: "
    ).strip()

    try:

        # Extract text
        text = extract_text(file_path)

        print("\n" + "=" * 60)
        print("TEXT EXTRACTION SUCCESSFUL")
        print("=" * 60)

        print("\nRaw characters:")
        print(len(text))

        # Clean text
        cleaned_text = clean_text(text)

        print("\nCleaned characters:")
        print(len(cleaned_text))

        # Save
        output_path = save_text(
            cleaned_text,
            file_path
        )

        print("\nText saved to:")
        print(output_path)

        print("\nFirst 1000 characters:")
        print("-" * 60)

        print(cleaned_text[:1000])

        print("\n" + "=" * 60)
        print("PARSER FINISHED")
        print("=" * 60)

    except Exception as e:

        print("\nERROR:")
        print(e)