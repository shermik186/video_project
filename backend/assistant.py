from dotenv import load_dotenv
from openai import AsyncOpenAI
from schemas import MoviesInput
from crud import load_genres, add_movies
from tools import create_testing_data
from tools import scan_new_relative_paths
import os


def get_ai_key():
    load_dotenv()
    return os.getenv("AI_KEY")


client = AsyncOpenAI(api_key=get_ai_key(), max_retries=5)


def get_genres():
    genres_set = load_genres()
    genre_text = ", ".join(genres_set)
    return genre_text


def get_paths_testing_data():
    paths_list = create_testing_data()
    paths_text = ", ".join(paths_list)
    return paths_text


async def get_response(paths_text, genre_text):

    response = await client.responses.parse(
        model="gpt-5.4-mini",
        instructions="""Jsi extraktor informací o filmech ze surových cest k souborům.

        Dostaneš seznam relative_path hodnot - cest k video souborům tak, jak jsou
        uložené na serveru. Pro KAŽDOU cestu ze seznamu proveď následující kroky
        a vrať výsledek jako seznam objektů (jeden objekt na jeden vstupní relative_path):
        
        1. Extrahuj čistý název filmu/seriálu ze souboru. Odstraň příponu, informace
           o kvalitě, rok, a nahraď tečky/podtržítka mezerami. Nepřekládej název,
           nezaměňuj ho za jiný podobný název, nepřidávej nic, co v původním názvu
           není. Cílem je pouze OČISTIT existující název, ne ho vymyslet znovu.
        
        2. Zkopíruj název složky, ve které je film uložen, PŘESNĚ A DOSLOVNĚ tak, jak je
            zapsaný na serveru - včetně veškerého číslování, podtržítek nebo prefixů.
            Neuprošťuj ho, neodstraňuj z něj žádnou část a neaplikuj na něj žádná
            pravidla čištění (na rozdíl od názvu filmu v bodě 1). Cílem je věrná kopie
            celého názvu složky beze změny.
        
        3. Přiřaď filmu 1 až 3 nejvýstižnější žánry. Vybírej VÝHRADNĚ ze seznamu
           žánrů, který ti bude poskytnut. Nikdy nevytvářej nový žánr ani lehce
           upravenou variantu existujícího žánru - pokud si nejsi jistý, vyber
           nejbližší odpovídající žánr ze seznamu.
        4. Do výstupního pole relative_path zkopíruj PŘESNĚ a DOSLOVNĚ tu hodnotu
            relative_path, ke které se tento výsledek vztahuje - bez jakékoliv
            úpravy, zkrácení nebo opravy. Slouží k jednoznačnému spárování výsledku
            zpět s původním souborem.
        """,
        input=f"Zde je seznam povolených žánarů: {genre_text}\n"
        f"a zde seznam relative_paths: {paths_text}",
        text_format=MoviesInput,
    )
    print(f"vraceno nových cest od AI: {len(response.output_parsed.items)}")

    return response.output_parsed


async def get_limited_response(batch_text, semaphore, genre_text):
    async with semaphore:
        movies = await get_response(batch_text, genre_text)
        add_movies(movies)
