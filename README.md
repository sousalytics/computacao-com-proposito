# Computação com Propósito — Template de Entregas (GitHub Pages + Python)

Este repositório **agrega** os projetos dos estudantes automaticamente (sem JS no cliente). 
Os grupos abrem **Pull Request** adicionando uma pasta em `projects/<CODIGO-DO-GRUPO>/` com:
- `meta.yml` — metadados (id, título, ODS, etc.)
- `summary.md` — resumo do projeto (markdown)
- opcional: `assets/` — imagens, PDFs, etc.

A publicação é feita via **GitHub Actions**: um script Python (ver `build.py`) lê as pastas em `projects/`, gera HTML estático em `site/` e a Action implanta no **GitHub Pages**.

> **Observação importante:** GitHub Pages não executa Python em tempo de execução. O Python roda **no build** (via Actions) para produzir HTML estático.


## Como os estudantes submetem
1. Faça um **fork** deste template, ou crie um repo a partir dele (Use this template).
2. Para cada grupo, crie um branch e **adiciona** a pasta `projects/<CODIGO-DO-GRUPO>/` com os arquivos descritos abaixo.
3. Abra um **Pull Request**. O workflow de build será executado e você verá o site pré-visualizado.
4. Ao aprovar/mergir na `main`, o site será publicado em **GitHub Pages** (com Actions).


## Estrutura do projeto
```
.
├── assets/
│   └── style.css
├── build.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html.j2
│   └── project.html.j2
├── projects/
│   └── sample-1A23/
│       ├── meta.yml
│       ├── summary.md
│       └── assets/ (opcional)
└── .github/workflows/build.yml
```

## Esquema do `meta.yml`
```yaml
id: "1A-23"             # código do grupo/líder
title: "Ouvidoria Segura — MVP"
topic: "Convivência"    # tema
ods: [4, 10, 17]        # ODS relacionadas
type: "web-static"      # web-static | form-planilha | script | outro
date: "2025-06-30"      # ISO (AAAA-MM-DD)
leaders: ["2025001"]    # matrícula(s) do(s) líder(es)
team: ["2025001", "2025002", "2025003"]
repo_url: ""            # opcional
demo_url: ""            # opcional
tags: ["ouvidoria", "ética", "privacidade"]
```

## Rodar localmente
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python build.py
# Abra site/index.html no navegador
```

## Publicação via GitHub Actions
- Ative **Pages** no repositório (Settings → Pages → Build and deployment: GitHub Actions).
- Ao fazer push na `main`, a Action:
  1) instala deps,
  2) roda `python build.py`,
  3) publica `site/` no Pages.

---

### Licenças sugeridas
- Conteúdos (textos/imagens dos alunos): **CC BY-SA**
- Código do template: **MIT**
