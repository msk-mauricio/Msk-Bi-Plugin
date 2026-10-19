"""Exporta a documentação Markdown da Fase 8 para HTML e PDF (padrão D-25).

Uso:
    python exportar_docs.py <pasta-com-md> [--titulo "Nome do Projeto"]

Para cada <arquivo>.md da pasta (sem recursão) gera:
    <pasta>/html/<arquivo>.html   página autocontida (CSS embutido, sem dependência externa)
    <pasta>/pdf/<arquivo>.pdf     impresso pelo Microsoft Edge em modo headless
e um <pasta>/html/index.html com links para todos os documentos.

Requisitos: Python 3 + pacote `markdown` (instalado automaticamente com pip --user se faltar)
e Microsoft Edge (padrão no Windows). Links entre documentos (.md) são reescritos para .html.
"""
import argparse
import datetime
import html
import os
import re
import subprocess
import sys

try:
    import markdown
except ImportError:  # instala uma vez e segue
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-q", "markdown"])
    import site
    sys.path.append(site.getusersitepackages())
    import markdown

EDGE_PATHS = [
    os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
    os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
]

CSS = """
:root{--brand:#367DD9;--brand2:#3299D9;--accent:#F2A516;--ink:#212121;--muted:#616161;--line:#E2E4E5;--zebra:#F6F8FB}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);font:14px/1.6 'Segoe UI',Arial,sans-serif}
header.doc{background:var(--brand);color:#fff;padding:20px 40px}
header.doc .proj{font-size:12px;opacity:.85;letter-spacing:.04em;text-transform:uppercase}
header.doc h1{margin:4px 0 0;font-size:24px;border:0;color:#fff}
main{max-width:1100px;margin:0 auto;padding:24px 40px 48px}
h1,h2,h3,h4{color:var(--brand);line-height:1.3}
h1{font-size:24px;border-bottom:3px solid var(--accent);padding-bottom:6px}
h2{font-size:20px;border-bottom:1px solid var(--line);padding-bottom:4px;margin-top:32px}
h3{font-size:16px;color:var(--brand2)}
h4{font-size:14px;color:var(--brand2)}
a{color:var(--brand)}
code{font-family:Consolas,'Cascadia Mono',monospace;font-size:12.5px;background:#F1F3F5;padding:1px 4px;border-radius:3px}
pre{background:#F1F3F5;border:1px solid var(--line);border-radius:6px;padding:12px;overflow-x:auto;white-space:pre-wrap;word-break:break-word}
pre code{background:none;padding:0}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:12.5px}
th{background:var(--brand);color:#fff;text-align:left;padding:6px 8px;font-weight:600}
th code{background:rgba(255,255,255,.18);color:#fff}
td{border-bottom:1px solid var(--line);padding:5px 8px;vertical-align:top}
tr:nth-child(even) td{background:var(--zebra)}
blockquote{margin:12px 0;padding:8px 14px;border-left:4px solid var(--accent);background:#FFF8EA;color:var(--muted)}
.toc{background:var(--zebra);border:1px solid var(--line);border-radius:6px;padding:10px 18px;margin:16px 0}
.toc ul{margin:4px 0;padding-left:18px}
footer.doc{color:var(--muted);font-size:11px;border-top:1px solid var(--line);margin-top:40px;padding-top:8px}
.index li{margin:6px 0}
@media print{
  @page{size:A4;margin:16mm 14mm}
  body{font-size:11px}
  header.doc{padding:12px 0;background:none;color:var(--brand);border-bottom:3px solid var(--accent)}
  header.doc h1{color:var(--brand)}
  main{max-width:none;padding:0}
  h2{break-after:avoid}
  table,pre,blockquote{break-inside:auto}
  tr{break-inside:avoid}
  a{color:inherit;text-decoration:none}
}
"""

PAGE = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{css}</style></head>
<body><header class="doc"><div class="proj">{proj}</div><h1>{title}</h1></header>
<main>{body}<footer class="doc">Gerado em {data} a partir de <code>{fonte}</code>.</footer></main></body></html>
"""


def titulo_do_md(texto, fallback):
    m = re.search(r"^#\s+(.+)$", texto, re.M)
    return m.group(1).strip() if m else fallback


def md_para_html(texto):
    # links para outros .md viram .html (mantém âncoras)
    texto = re.sub(r"\]\(([^)\s]+?)\.md(#[^)]*)?\)", lambda m: "](%s.html%s)" % (m.group(1), m.group(2) or ""), texto)
    # Python-Markdown exige linha em branco antes de lista; os .md do kit nem sempre têm
    linhas, saida, em_codigo = texto.split("\n"), [], False
    for ln in linhas:
        if ln.lstrip().startswith("```"):
            em_codigo = not em_codigo
        eh_item = re.match(r"\s*([-*+]|\d+\.)\s+", ln)
        if (not em_codigo and eh_item and saida and saida[-1].strip()
                and not re.match(r"\s*([-*+]|\d+\.)\s+", saida[-1]) and not saida[-1].lstrip().startswith("|")):
            saida.append("")
        saida.append(ln)
    texto = "\n".join(saida)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"],
                           extension_configs={"toc": {"permalink": False}})
    corpo = md.convert(texto)
    # remove o primeiro H1 (já vai no cabeçalho)
    corpo = re.sub(r"^\s*<h1[^>]*>.*?</h1>", "", corpo, count=1, flags=re.S)
    return corpo


def imprimir_pdf(edge, html_path, pdf_path):
    url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    cmd = [edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           "--print-to-pdf=" + os.path.abspath(pdf_path), url]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--titulo", default="")
    a = ap.parse_args()
    pasta = os.path.abspath(a.pasta)
    proj = a.titulo or os.path.basename(os.path.dirname(os.path.dirname(pasta))) or "Documentação"
    out_html = os.path.join(pasta, "html")
    out_pdf = os.path.join(pasta, "pdf")
    os.makedirs(out_html, exist_ok=True)
    os.makedirs(out_pdf, exist_ok=True)
    edge = next((p for p in EDGE_PATHS if os.path.exists(p)), None)
    data = datetime.date.today().strftime("%d/%m/%Y")

    docs, falhas = [], []
    for nome in sorted(os.listdir(pasta)):
        if not nome.lower().endswith(".md"):
            continue
        base = nome[:-3]
        texto = open(os.path.join(pasta, nome), encoding="utf-8").read()
        titulo = titulo_do_md(texto, base)
        pagina = PAGE.format(title=html.escape(titulo), css=CSS, proj=html.escape(proj), body=md_para_html(texto),
                             data=data, fonte=html.escape(nome))
        hp = os.path.join(out_html, base + ".html")
        open(hp, "w", encoding="utf-8").write(pagina)
        ok_pdf = imprimir_pdf(edge, hp, os.path.join(out_pdf, base + ".pdf")) if edge else False
        if not ok_pdf:
            falhas.append(nome)
        docs.append((base, titulo, ok_pdf))

    itens = "".join('<li><a href="%s.html">%s</a> &nbsp;·&nbsp; <a href="../pdf/%s.pdf">PDF</a></li>'
                    % (b, html.escape(t), b) for b, t, _ in docs)
    idx = PAGE.format(title="Documentação do projeto", css=CSS, proj=html.escape(proj),
                      body='<ul class="index">%s</ul>' % itens, data=data, fonte=os.path.basename(pasta) + "/*.md")
    open(os.path.join(out_html, "index.html"), "w", encoding="utf-8").write(idx)

    print("HTML: %d arquivo(s) em %s" % (len(docs), out_html))
    print("PDF : %d arquivo(s) em %s" % (len(docs) - len(falhas), out_pdf))
    if not edge:
        print("AVISO: Microsoft Edge não encontrado — PDFs não gerados.")
    elif falhas:
        print("AVISO: PDF não gerado para: " + ", ".join(falhas))
        sys.exit(2)


if __name__ == "__main__":
    main()
