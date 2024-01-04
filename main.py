from nicegui import ui
from Api.TmdbApi import TmdbAPI
from Models import item_card, nav_bar

tmdb_api = TmdbAPI()


@ui.page("/")
async def home_page(page_no: int = 1):
    movies = await tmdb_api.discover_movies(page_no=page_no)
    items = movies["items"]

    nav_bar.init_navbar()

    ui.input(label="Search Movies").props("rounded outlined dense size=100")

    with ui.grid(columns=6):
        for item in items:
            item_card.item_card(
                title=item["title"],
                poster=item["poster"],
                href=item["id"],
                release_date=item["release_date"],
                ratings=item["ratings"],
            )

    ui.pagination(
        1,
        40,
        direction_links=True,
        on_change=lambda x: ui.open(f"/?page_no={x.value}"),
        value=page_no,
    )


@ui.page("/shows")
async def home_page(page_no: int = 1):
    movies = await tmdb_api.discover_shows(page_no=page_no)
    items = movies["items"]

    nav_bar.init_navbar()

    ui.input(label="Search Tv Shows").props("rounded outlined dense size=100")

    with ui.grid(columns=6):
        for item in items:
            item_card.item_card(
                title=item["title"],
                poster=item["poster"],
                href=item["id"],
                mode="shows",
                release_date=item["release_date"],
                ratings=item["ratings"],
            )

    ui.pagination(
        1,
        40,
        direction_links=True,
        on_change=lambda x: ui.open(f"/shows?page_no={x.value}"),
        value=page_no,
    )


ui.run(port=5000)
