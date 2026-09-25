# HR Assistant — RAG for Candidate Screening

An HR assistant built with RAG (Retrieval-Augmented Generation) techniques that analyzes a resume archive and answers natural-language questions about which candidate best fits a position, using semantic search over a vector database.

## How it works

- Resumes are read from the `resumes/` folder, split into semantic chunks, and indexed in **ChromaDB**.
- On every startup the system automatically syncs the database with the files on disk: it computes an MD5 hash of each resume and adds, updates, or removes only what has changed (see [Sync strategy](#sync-strategy)).
- User questions are matched against the indexed chunks via semantic search; the most relevant context is passed to a language model (OpenAI or local Ollama) to generate the answer.
- The chat interface is built with **Chainlit** and includes quick actions to check database stats or force a reindex.

## Stack

- [Chainlit](https://docs.chainlit.io) — conversational interface
- [ChromaDB](https://www.trychroma.com/) — vector database
- [OpenAI API](https://platform.openai.com/) / [Ollama](https://ollama.com/) — language models (cloud or local)
- [scikit-learn](https://scikit-learn.org/) — semantic chunking support
- [Poetry](https://python-poetry.org/) — dependency management

## Installation

```bash
poetry install
eval $(poetry env activate)
```

If `poetry add` throws a version compatibility error, check that `pyproject.toml` has:

```toml
requires-python = ">=3.13,<4.0.0"
```

## Configuration

Create a `.env` file in the project root with your OpenAI key:
```
OPENAI_API_KEY=sk-...
```


## Running

```bash
chainlit run hr_assistant/__init__.py -w
```

## Running local models (optional)

As an alternative to OpenAI, you can use local models via [Ollama](https://ollama.com/):

```bash
ollama run llama3.2
# or, lighter and quite capable
ollama run deepseek-r1:1.5b
```

## Sync strategy

Each resume is tracked via an MD5 hash of its content, file name, and last-modified date. On startup, the system compares the files present in `resumes/` against what's already tracked in the database and automatically detects:

- **new files** → chunked and indexed;
- **modified files** → old chunks are removed and replaced with updated ones;
- **deleted files** → associated chunks are removed from the database.

This avoids duplication, reduces unnecessary writes, and keeps the database always aligned with the actual files — even after interruptions, since the system re-syncs automatically on the next run.

## Project structure
```
hr_assistant/
├── __init__.py              # entry point Chainlit, gestione chat e azioni
├── config.py                # configurazione
├── database.py               # interfaccia ChromaDB
├── document_processor.py     # sync e processing dei CV
├── semantic_chunking.py       # logica di chunking semantico
└── utils.py                   # helper per le chiamate al modello linguistico

resumes/                       # CV di esempio (dati fittizi)
data/chromadb/                  # database vettoriale (generato, non versionato)
```

## Notes

The resumes in the `resumes/` folder are fictional sample data used for testing and demonstration purposes.

-------------------------------------------------------------------------------------

# HR Assistant — RAG per la selezione dei candidati

Un assistente HR basato su tecniche RAG (Retrieval-Augmented Generation) che analizza un archivio di CV e risponde in linguaggio naturale a domande su quale candidato è più adatto a una posizione, usando ricerca semantica su un database vettoriale.

## Come funziona

- I CV vengono letti dalla cartella `resumes/`, suddivisi in chunk semantici e indicizzati in **ChromaDB**.
- Ad ogni avvio il sistema sincronizza automaticamente il database con i file presenti: calcola l'hash MD5 di ogni CV e aggiunge, aggiorna o rimuove solo ciò che è cambiato (vedi sezione [Strategia di sync](#strategia-di-sync-dei-file)).
- Le domande dell'utente vengono confrontate con i chunk indicizzati tramite ricerca semantica; il contesto più rilevante viene passato a un modello linguistico (OpenAI o Ollama in locale) che genera la risposta.
- L'interfaccia chat è realizzata con **Chainlit** e include azioni rapide per consultare le statistiche del database o forzare una reindicizzazione.

## Stack

- [Chainlit](https://docs.chainlit.io) — interfaccia conversazionale
- [ChromaDB](https://www.trychroma.com/) — database vettoriale
- [OpenAI API](https://platform.openai.com/) / [Ollama](https://ollama.com/) — modelli linguistici (cloud o locale)
- [scikit-learn](https://scikit-learn.org/) — supporto al chunking semantico
- [Poetry](https://python-poetry.org/) — gestione dipendenze

## Installazione

```bash
poetry install
eval $(poetry env activate)
```

Se `poetry add` restituisce un errore di compatibilità versioni, verifica che nel `pyproject.toml` sia impostato:

```toml
requires-python = ">=3.13,<4.0.0"
```

## Configurazione

Crea un file `.env` nella root del progetto con la tua chiave OpenAI:

```
OPENAI_API_KEY=sk-...
```

## Esecuzione

```bash
chainlit run hr_assistant/__init__.py -w
```

## Esecuzione di modelli in locale (opzionale)

In alternativa a OpenAI, è possibile usare modelli locali via [Ollama](https://ollama.com/):

```bash
ollama run llama3.2
# oppure, più leggero e potente
ollama run deepseek-r1:1.5b
```

## Strategia di sync dei file

Ogni CV viene tracciato tramite hash MD5 del contenuto, nome file e data di ultima modifica. All'avvio il sistema confronta i file presenti in `resumes/` con quelli già tracciati nel database e individua automaticamente:

- **file nuovi** → vengono suddivisi in chunk e indicizzati;
- **file modificati** → i vecchi chunk vengono rimossi e sostituiti con quelli aggiornati;
- **file eliminati** → i chunk associati vengono rimossi dal database.

Questo evita duplicazioni, riduce le scritture inutili e mantiene il database sempre allineato ai file reali, anche in caso di interruzioni: alla riesecuzione successiva il sistema si risincronizza automaticamente.

## Struttura del progetto

```
hr_assistant/
├── __init__.py              # entry point Chainlit, gestione chat e azioni
├── config.py                # configurazione
├── database.py               # interfaccia ChromaDB
├── document_processor.py     # sync e processing dei CV
├── semantic_chunking.py       # logica di chunking semantico
└── utils.py                   # helper per le chiamate al modello linguistico

resumes/                       # CV di esempio (dati fittizi)
data/chromadb/                  # database vettoriale (generato, non versionato)
```

## Note

I CV nella cartella `resumes/` sono dati di esempio fittizi, usati per test e dimostrazione.
