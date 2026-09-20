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
