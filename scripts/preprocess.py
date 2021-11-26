import xml.etree.ElementTree as ET
import os
from pathlib import Path
from typing import List
import re
import spacy
import typer
from spacy.language import Language
from spacy.tokens import Doc, DocBin
from spacy.util import filter_spans
from wasabi import msg


def main(
    input_dir: Path = typer.Argument(..., exists=True),
    output_dir: Path = typer.Argument(...),
    test_dir: Path = typer.Argument(..., exists=True)
):

    msg.info("Converting to spaCy Doc objects.")

    train_docs = docs_from_xml_files(input_dir)

    split_idx = int(len(train_docs) * 0.80)

    train_docs, dev_docs = train_docs[:split_idx], train_docs[split_idx:]

    test_docs = docs_from_xml_files(test_dir)

    msg.good(f"Num Train Docs: {len(train_docs)}")
    msg.good(f"Num Dev Docs: {len(dev_docs)}")
    msg.good(f"Num Test Docs: {len(test_docs)}")

    with msg.loading(f"Saving docs to: {output_dir}..."):
        DocBin(docs=train_docs).to_disk(output_dir / "train.spacy")
        DocBin(docs=dev_docs).to_disk(output_dir / "dev.spacy")
        DocBin(docs=test_docs).to_disk(output_dir / "test.spacy")
        msg.good("Done.")


def docs_from_xml(
    text: str, annotations: List[str], nlp: Language
) -> List[Doc]:
    '''
        Criar um Doc spaCy de um documento anotado
        text (str): texto dos dados
        annotations (List[str]): dados de entidades anotadas, obtidos do XML
        nlp (Language): objeto Language do spaCy. Default é spacy.blank('en')

        retorna (List[Doc]): lista de Docs spaCy contendo um único Doc
    '''

    full_text = text

    docs = []
    doc = nlp.make_doc(text)
    spans = []

    invalid_span_tokens = re.compile(r'\s')

    for row in annotations:
        annotation = row.attrib
        start = int(annotation['start'])
        end = int(annotation['end'])
        category = annotation['TYPE']

        valid_start = start
        valid_end = end

        while valid_start < len(text) and invalid_span_tokens.match(full_text[valid_start]):
            valid_start += 1
        while valid_end > 1 and invalid_span_tokens.match(full_text[valid_end - 1]):
            valid_end -= 1

        spans.append((valid_start, valid_end, category))

    ents = [
        doc.char_span(start, end, label=label)
        for (start, end, label) in spans
    ]

    ents = [e for e in ents if e is not None]

    doc.ents = filter_spans(ents)

    docs.append(doc)

    return docs


def docs_from_xml_files(
    base_path: Path, nlp: Language = spacy.blank('en')
) -> List[Doc]:
    all_docs = []

    for file in os.listdir(base_path):
        mytree = ET.parse(base_path / file)
        myroot = mytree.getroot()
        text = myroot.find('.//TEXT')
        file_content = text.text
        tags = myroot.find('.//TAGS')

        docs = docs_from_xml(file_content, tags, nlp)
        all_docs += docs

    return all_docs


if __name__ == '__main__':
    typer.run(main)
