import json
from pathlib import Path

import pymupdf
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document


def extract_images_from_pdf(
    file_path: str | Path,
    output_dir: str | Path | None = None,
    password: str | None = None,
) -> list[dict[str, int | str]]:
    """Extract embedded PDF images and save them, returning their page and paths."""
    pdf_path = Path(file_path).expanduser()
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF file does not exist: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Unsupported file type: {pdf_path.suffix or 'no extension'}")

    image_dir = (
        Path(output_dir).expanduser()
        if output_dir is not None
        else pdf_path.parent / f"{pdf_path.stem}_images"
    )
    extracted_images: list[dict[str, int | str]] = []

    with pymupdf.open(str(pdf_path)) as pdf:
        if pdf.is_encrypted and (password is None or not pdf.authenticate(password)):
            raise ValueError(f"PDF is encrypted or the password is incorrect: {pdf_path}")

        for page_index, page in enumerate(pdf):
            image_index = 0
            for image_info in page.get_images(full=True):
                image_data = pdf.extract_image(image_info[0])
                image_bytes = image_data.get("image")
                if not image_bytes:
                    continue

                image_dir.mkdir(parents=True, exist_ok=True)
                extension = str(image_data.get("ext", "bin"))
                if not extension.isalnum():
                    extension = "bin"
                image_path = image_dir / (
                    f"page_{page_index + 1:04d}_image_{image_index + 1:03d}.{extension}"
                )
                image_path.write_bytes(image_bytes)
                extracted_images.append(
                    {"page": page_index, "path": str(image_path.resolve())}
                )
                image_index += 1

    return extracted_images


def load_document(
    file_path: str | Path,
    image_output_dir: str | Path | None = None,
    password: str | None = None,
) -> list[Document]:
    """Load PDF page text and extract its images for downstream RAG processing."""
    pdf_path = Path(file_path).expanduser()
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF file does not exist: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Unsupported file type: {pdf_path.suffix or 'no extension'}")

    documents = PyMuPDFLoader(pdf_path, password=password).load()
    images_by_page: dict[int, list[str]] = {}
    for image in extract_images_from_pdf(
        pdf_path, output_dir=image_output_dir, password=password
    ):
        images_by_page.setdefault(int(image["page"]), []).append(str(image["path"]))

    for document in documents:
        page = document.metadata.get("page")
        if isinstance(page, int) and page in images_by_page:
            document.metadata["image_paths"] = json.dumps(images_by_page[page])

    return documents
