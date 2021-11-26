# :ringed_planet: spaCy Project: Detecting PHI in medical records (Named Entity Recognition)

## :books: Summary

| Section                                                 |                                                          |
|---------------------------------------------------------|----------------------------------------------------------|
| :clipboard: **[project.yml]**                           | File for project configuration.                          |
| :green_book: **[Models]**                               | Models pipelines that can be used                        |
| :pencil: **[Using custom transformers]**                | Customize the transformer model                          |
| :play_or_pause_button: **[Commands]**                   | Commands to execute the workflow steps                   |
| :next_track_button: **[Workflows]**                     | Complete workflows from preprocessing to anonymization   |
| :card_index_dividers: **[Assets]**                      | Project files for training and evaluation                |
| :dvd: **[Installation - Windows]**                      | Steps to install all tools on Windows environment        |
| :zap: **[Redacting TXT and PDF documents]**             | Perform anonymization on documents                       |     
| :crystal_ball: **[Model results]**                      | View model metrics from evaluations                      |

[project.yml]: #clipboard-projectyml
[Models]: #green_book-models
[Using custom transformers]: #pencil-using-custom-transformers
[Commands]: #play_or_pause_button-commands
[Workflows]: #next_track_button-workflows
[Assets]: #card_index_dividers-assets
[Installation - Windows]: #dvd-installation---windows
[Model results]: #crystal_ball-model-results
[Redacting TXT and PDF documents]: #zap-redacting-txt-and-pdf-documents

### :clipboard: project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. 

### :green_book: Models
| Model                 | NER pipeline  | Technique                   |
| ----------------------|---------------|-----------------------------|
| spacy-vectors         | spaCy ner     | en_core_web_md Vectors      |
| spacy-trf             | spaCy ner     | Custom Transformers         |

### :pencil: Using custom transformers
To use a custom transformer model, find the name of the transformer from [Hugging Face's Pretrained models library](https://huggingface.co/transformers/pretrained_models.html) and put the model name on the `configs/config_spacy_trf.cfg` file on the `[components.transformer.model]` section.

### :play_or_pause_button: Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command               | Description                                                   |
| ----------------------|---------------------------------------------------------------|
| `preprocess`          | Convert the data to spaCy's binary format                     |
| `train-<model>`       | Train the specified NER model                                 |
| `evaluate-<model>`    | Evaluate the specified NER model and export metrics           |
| `package-<model>`     | Package the specified trained model so it can be installed    |
| `anonymize`           | Run the anonymizer on input files using the packaged model    |

### :next_track_button: Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow          | Steps                                                                             |
| ------------------|-----------------------------------------------------------------------------------|
| `spacy-vectors`   | `preprocess` &rarr; `train-spacy-vectors`     &rarr; `evaluate-spacy-vectors`     |
| `spacy-trf`       | `preprocess` &rarr; `train-spacy-trf`         &rarr; `evaluate-spacy-trf`         |

### :card_index_dividers: Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File                                  | Source    | Description                               |
|---------------------------------------|-----------|-------------------------------------------|
| `assets/i2b2/testing-PHI-Gold-fixed`  | Local     | Folder containing XML testing files       |
| `assets/i2b2/training-PHI-Gold-Set1`  | Local     | Folder containing XML training files      |

### :dvd: Installation - Windows

1. [Install CUDA Toolkit 11.1.0](https://developer.nvidia.com/cuda-11.1.0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exelocal)

2. Create virtual environment and install spaCy
```bash
python -m venv env
env\Scripts\activate
pip install pip setuptools wheel
pip install spacy[cuda111,transformers,lookups]
python -m spacy download en_core_web_md
```

3. [Install PyTorch with command from "Start Locally" on website (Stable Version, Pip, Python, CUDA 11.1)](https://pytorch.org/get-started/locally/)

4. Install spaCy transformers and PDF manipulation tools
```bash
pip install spacy-transformers
pip install PyMuPDF==1.19.1
```

5. Test GPU is accessible by PyTorch and spaCy (on Python shell)
```python
import torch
torch.cuda.is_available()
import spacy
spacy.require_gpu()
```

### :zap: Redacting TXT and PDF documents

1. Make sure the trained model was packaged with the `spacy project run package-<model>` command

2. Place `.txt` and `.pdf` files on folder `assets/input_documents`

3. Run `spacy project run anonymize`

4. Check folder `assets/output_documents` for anonymized documents

### :crystal_ball: Model results
| Number | ML Technique           | Model pipeline                        | Precision | Recall | F-Score |
|:------:|------------------------|---------------------------------------|:---------:|:------:|:-------:|
| #1     | :fire: Word vectors    | en_core_web_md                        | 90.66     | 81.64  | 85.92   |
| #2     | :comet: Transformers   | roberta-base                          | 77.47     | 87.04  | 81.97   |
| #3     | :comet: Transformers   | bert-base-cased                       | 89.29	  | 82.05  | 85.52   |
| #4     | :comet: Transformers   | bert-base-uncased                     | 90.85	  | 79.91  | 85.03   |
| #5     | :comet: Transformers   | bert-base-multilingual-cased          | 90.41	  | 82.01  | 86.01   |
| #6     | :comet: Transformers   | bert-base-multilingual-uncased        | 89.03	  | 82.47  | 85.62   |
| #7     | :comet: Transformers   | distilbert-base-uncased               | 88.28     | 80.99  | 84.48   |
| #8     | :comet: Transformers   | albert-base-v1                        | 88.90     | 47.00  | 61.49   |
| #9     | :comet: Transformers   | albert-base-v2                        | 86.95	  | 44.07  | 58.49   |
| #10    | :comet: Transformers   | camembert-base                        | 88.48	  | 79.56  | 83.78   |
| #11    | :comet: Transformers   | flaubert/flaubert_base_uncased        | 83.32     | 51.95  | 64.00   |
| #12    | :comet: Transformers   | microsoft/layoutlm-base-uncased       | 87.35	  | 80.65  | 83.87   |
| #13    | :comet: Transformers   | squeezebert/squeezebert-uncased       | 82.66	  | 78.45  | 80.50   |
| #14    | :comet: Transformers   | squeezebert/squeezebert-mnli          | 81.58	  | 75.08  | 78.20   |