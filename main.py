from nicegui import ui
from Api.TmdbApi import TmdbAPI
from Models import item_card

tmdb_api = TmdbAPI()


@ui.page("/")
async def home_page(page_no: int = 1):
    movies = await tmdb_api.discover_movies(page_no=page_no)

    max_pages = movies["max_pages"]
    items = movies["items"]

    ui.input(label="Search Movies").props("rounded outlined dense size=100")

    with ui.grid(columns=6):
        for item in items:
            item_card.item_card(item["title"], item["poster"], item["id"])

    ui.pagination(
        1,
        10,
        direction_links=True,
        on_change=lambda x: ui.open(f"/?page_no={x.value}"),
        value=page_no,
    )


ui.run(port=5000)
