from pathlib import Path
import typer
import spacy
import os
import fitz
from spacy.language import Language
from wasabi import msg


def process_pdf(
    file_path: Path, nlp: Language,
    output_dir: Path
):
    file_name = os.path.basename(file_path)
    msg.info("Processing PDF file: " + file_name)

    try:
        document = fitz.open(file_path)
        for page in document:
            page.wrapContents()
            text = page.getText('text')
            doc = nlp(text)
            redact = []

            for ent in doc.ents:
                redact.append(ent.text)

            for data in redact:
                rects = page.searchFor(data)
                for rect in rects:
                    page.addRedactAnnot(
                        rect,
                        text=data,
                        fill=(0, 0, 0)
                    )
            page.apply_redactions()
        msg.good("Saving redacted file: " + file_name)
        document.save(output_dir / file_name)
    except Exception as _e:
        msg.fail(f"Error while processing file {file_name}: {_e}")


def process_txt(
    file_path: Path, nlp: Language,
    output_dir: Path
):
    file_name = os.path.basename(file_path)
    msg.info("Processing TXT file: " + file_name)
    with open(file_path) as f:
        text = f.read()
        doc = nlp(text)
        for ent in doc.ents:
            text = text.replace(ent.text, f"<{ent.label_}>")

        with open(output_dir / file_name, 'w') as output_file:
            output_file.write(text)


def main(
    model_dir: Path = typer.Argument(..., exists=True),
    input_dir: Path = typer.Argument(..., exists=True),
    output_dir: Path = typer.Argument(...)
):
    msg.info("Loading spaCy model.")

    nlp = spacy.load(model_dir)

    msg.info("Processing input files.")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        msg.good("Created output folder: " + str(output_dir))

    for file in os.listdir(input_dir):
        msg.warn(f"File: {file}")
        if file.endswith('.pdf'):
            process_pdf(input_dir / file, nlp, output_dir)
        elif file.endswith('.txt'):
            process_txt(input_dir / file, nlp, output_dir)


if __name__ == '__main__':
    typer.run(main)
