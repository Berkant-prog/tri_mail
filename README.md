# Mail Agent

Squelette d'un agent de tri et de rédaction de mails basé sur LangGraph. Les
nœuds contiennent uniquement les contrats et stubs nécessaires pour étendre la
logique métier.

## Installation

Le projet utilise `uv` et `pyproject.toml` :

```powershell
uv sync
```

Les dépendances de développement, dont `pytest`, sont installées par la commande
ci-dessus. Pour utiliser Poetry, le `pyproject.toml` peut être repris comme
base, mais les commandes documentées ici sont celles de `uv`.

## Configuration

Copiez `.env.example` vers `.env`, puis renseignez au minimum `POSTGRES_DSN` et
les chemins OAuth Google. Placez les identifiants Google attendus par Gmail API
dans le chemin indiqué par `GOOGLE_CLIENT_SECRET_FILE`. Les champs du fichier
`.env` sont chargés par `pydantic-settings`.

Pour activer le suivi LangSmith, renseignez `LANGSMITH_API_KEY`, laissez
`LANGSMITH_TRACING=true`, puis choisissez éventuellement un nom avec
`LANGSMITH_PROJECT`. LangChain et LangGraph détectent automatiquement ces
variables et envoient les traces des exécutions au projet LangSmith configuré.
Ne mettez jamais la clé dans `.env.example` ni dans Git.

## Lancer l'API

Depuis la racine du projet :

```powershell
uv run uvicorn mail_agent.api.main:app --reload
```

La route de reprise après interruption est disponible sur
`POST /runs/{thread_id}/resume`. Elle accepte un objet JSON de décision et
reprendra le graphe via `Command(resume=...)` lorsque le checkpointer Postgres
sera branché dans `mail_agent/graph.py`.

## Tests

```powershell
uv run pytest
```
