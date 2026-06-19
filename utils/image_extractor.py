import fitz
import os
from docx import Document


def extract_images(file_path):

    images = []

    folder = "temp/page_images"

    os.makedirs(
        folder,
        exist_ok=True
    )

    # ====================
    # PDF
    # ====================

    if file_path.lower().endswith(".pdf"):

        pdf = fitz.open(
            file_path
        )

        for page_num in range(
            len(pdf)
        ):

            page = pdf[
                page_num
            ]

            pix = page.get_pixmap(
                matrix=fitz.Matrix(
                    2,
                    2
                )
            )

            out = (
                f"{folder}/page_{page_num+1}.png"
            )

            pix.save(
                out
            )

            images.append(
                out
            )

        pdf.close()

    # ====================
    # DOCX
    # ====================

    elif file_path.lower().endswith(".docx"):

        doc = Document(
            file_path
        )

        count = 0

        for rel in (
            doc.part.rels.values()
        ):

            if (
                "image"
                in rel.target_ref
            ):

                count += 1

                data = (
                    rel.target_part.blob
                )

                out = (
                    f"{folder}/doc_img_{count}.png"
                )

                with open(
                    out,
                    "wb"
                ) as f:

                    f.write(
                        data
                    )

                images.append(
                    out
                )

    return images