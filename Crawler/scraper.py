import asyncio
import json
import httpx
import lxml.html
import lxml.etree
from lxml.html import HtmlElement
import re

main_url = "https://sol.sbc.org.br/index.php/stil/issue/view/1383"


def get_selector(html: HtmlElement, xpath: str):
    if sel := html.xpath(xpath):
        return sel[0]
    return None


def getall_selector(html: HtmlElement, xpath: str):
    if sel := html.xpath(xpath):
        return sel
    return None


def strip(val: str | list):
    if not val:
        return None
    if isinstance(val, list):
        return [v.strip() for v in val if v.strip()]
    return val.strip() if val.strip() else None


async def fetch_page(_url):
    print(f"[LOG] Buscando página: {_url}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(_url)
            response.raise_for_status()
            txt = response.text
            print(f"[LOG] Página carregada com sucesso: {_url}")
        except Exception as e:
            print(f"[ERRO] Falha ao buscar página ({_url}): {str(e)}")
            return None

    return lxml.html.fromstring(txt)


async def parse_section(html: HtmlElement):
    title = get_selector(html, "./h2/text()")
    print(f"[LOG] Iniciando parsing da seção: {strip(title)}")

    articles = getall_selector(html, "./ul/li")

    parsed_articles = []
    for idx, article in enumerate(articles):
        print(f"[LOG] Parsing artigo {idx + 1} na seção: {strip(title)}")
        parsed_articles.append(await parse_article(article))

    return {strip(title): parsed_articles}


async def parse_autor(html: HtmlElement):
    return dict(
        nome=strip(get_selector(html, "./span[1]/text()")),
        afiliacao=strip(get_selector(html, "./span[2]/text()")),
        orcid=strip(get_selector(html, "./span/a/text()")),
    )


async def parse_article_extra_info(html: HtmlElement):
    print("[LOG] Extraindo informações adicionais do artigo...")
    autores_xpath = getall_selector(html, ".//ul[@class = 'item authors']/li")

    authors = []
    for li in autores_xpath:
        authors.append(await parse_autor(li))

    publicado = strip(get_selector(html, ".//div[@class = 'item published']/div[@class='value']/text()"))
    resumo = strip(get_selector(html, ".//div[@class = 'item abstract']/p/text()"))
    keywords = get_selector(html, ".//div[@class = 'item keywords']/span[2]/text()")
    if keywords:
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    referencias = strip(getall_selector(html, ".//div[@class = 'item references']/div/text()"))
    referencias = [ref for ref in referencias if not re.search(r"DOI:", ref)]
    return dict(autores=authors, data_publicacao=publicado, resumo=resumo, keywords=keywords, referencias=referencias)


async def fetch_and_save_pdf(url: str):
    url = url.replace("view", "download")
    print(f"[LOG] Baixando PDF de: {url}")

    async with httpx.AsyncClient() as client:
        try:
            pdf_response = await client.get(url)
            pdf_response.raise_for_status()
            storage_key = f"files/article_{url.split('/')[-2]}_{url.split('/')[-1]}.pdf"
            with open(storage_key, "wb") as f:
                f.write(pdf_response.content)
            print(f"[LOG] PDF salvo em: {storage_key}")
            return storage_key
        except Exception as e:
            print(f"[ERRO] Erro ao tentar fazer download do PDF: {str(e)}")
            return "N/A"


async def parse_article(html: HtmlElement):
    print("[LOG] Iniciando parsing de um artigo...")
    titulo = get_selector(html, "./div/div/a")
    link_info = strip(get_selector(titulo, "./@href"))
    nome = strip(get_selector(titulo, "./text()"))

    print(f"[LOG] Título do artigo: {nome}")
    page_info = await fetch_page(link_info)

    if not page_info:
        print(f"[ERRO] Não foi possível carregar a página de informações do artigo: {link_info}")
        return {}

    extra_info = await parse_article_extra_info(page_info)

    pdf = get_selector(html, ".//li/a")
    pdf_link = strip(get_selector(pdf, "./@href"))
    pdf_label = strip(get_selector(pdf, "./text()"))
    idioma = "Inglês" if re.search(r"english", pdf_label, re.I) else "Português"

    storage_key = await fetch_and_save_pdf(pdf_link)

    article = dict(titulo=nome, informacoes_url=link_info, idioma=idioma, storage_key=storage_key)
    article.update(extra_info)

    return article


async def main():
    print(f"[LOG] Iniciando crawler na URL principal: {main_url}")
    main_page = await fetch_page(main_url)

    if not main_page:
        print("[ERRO] Página principal não foi carregada. Encerrando.")
        return

    sections = getall_selector(main_page, "//div[@class = 'sections']/div[@class='section']")
    if not sections:
        print("[ERRO] Nenhuma seção encontrada na página.")
        return

    parsed = dict()
    for idx, section in enumerate(sections):
        print(f"[LOG] Processando seção {idx + 1} de {len(sections)}")
        parsed.update(await parse_section(section))

    with open("artigos_serializados.json", "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=4)

    print(
        "[LOG] Crawler finalizado com sucesso.\n Arquivo 'artigos_serializados.json' salvo e pdfs salvos na pasta"
        " 'files'."
    )


if __name__ == "__main__":
    asyncio.run(main())
