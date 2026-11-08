from database import engine
from models import Base
from assistant import  get_limited_response
from crud import  load_genres
from tools import get_paths, turn_list_to_text
import asyncio


async def adding_script():
    Base.metadata.create_all(engine)
    semaphore = asyncio.Semaphore(3)

    all_paths = get_paths()
    batch_size = 15
    batched_text = []
    for i in range(0, len(all_paths), batch_size):
        batch = all_paths[i : i + batch_size]
        batch_text = turn_list_to_text(batch)
        batched_text.append(batch_text)

    genre_text = load_genres()
    coros = [get_limited_response(text, semaphore, genre_text) for text in batched_text]
    await asyncio.gather(*coros)


if __name__ == "__main__":
    asyncio.run(adding_script())