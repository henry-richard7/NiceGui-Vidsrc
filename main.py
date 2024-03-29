from nicegui import ui
from Api.TmdbApi import TmdbAPI
from Models import item_card, nav_bar

tmdb_api = TmdbAPI()


@ui.page("/")
async def home_page(page_no: int = 1):
    movies = await tmdb_api.discover_movies(page_no=page_no)
    items = movies["items"]

    nav_bar.init_navbar()

    with ui.row():
        query = ui.input(label="Search Movies").props("rounded outlined dense size=100")
        ui.button(
            icon="search",
            text="Search",
            on_click=lambda x: ui.open(f"/search?mode=movie&query={query.value}"),
        )

    with ui.grid(columns=6):
        for item in items:
            item_card.item_card(
                title=item["title"],
                poster=item["poster"],
                href=item["id"],
                release_date=item["release_date"],
                ratings=item["ratings"],
                adult=item["adult"],
            )

    ui.pagination(
        1,
        page_no + 10,
        direction_links=True,
        on_change=lambda x: ui.open(f"/?page_no={x.value}"),
        value=page_no,
    )


@ui.page("/shows")
async def tv_shows(page_no: int = 1):
    movies = await tmdb_api.discover_shows(page_no=page_no)
    items = movies["items"]

    nav_bar.init_navbar()

    with ui.row():
        query = ui.input(label="Search Tv Shows").props(
            "rounded outlined dense size=100"
        )
        ui.button(
            icon="search",
            text="Search",
            on_click=lambda x: ui.open(f"/search?mode=tv&query={query.value}"),
        )

    with ui.grid(columns=6):
        for item in items:
            item_card.item_card(
                title=item["title"],
                poster=item["poster"],
                href=item["id"],
                mode="shows",
                release_date=item["release_date"],
                ratings=item["ratings"],
                adult=item["adult"],
            )

    ui.pagination(
        1,
        page_no + 10,
        direction_links=True,
        on_change=lambda x: ui.open(f"/shows?page_no={x.value}"),
        value=page_no,
    )


@ui.page("/watch_movie")
async def watch_movie(tmdb_id):
    nav_bar.init_navbar()
    movie_details = await tmdb_api.get_movie_details(tmdb_id)

    ui.image(movie_details["banner"]).classes("h-80")
    with ui.grid(columns=3):
        ui.image(movie_details["poster"]).props("fit=scale-down").classes("w-[25vw]")
        with ui.column():
            ui.label(movie_details["title"]).classes("text-h5")
            ui.label("Description:").classes("text-h6")
            ui.label(movie_details["plot"])
            ui.label("Casts:").classes("text-h6")
            with ui.scroll_area().classes("w-[30vw]"):
                with ui.row():
                    for cast in movie_details["casts"]:
                        with ui.image(cast["photo"]).classes("w-[8vw]"):
                            ui.label(cast["name"]).classes(
                                "absolute-bottom text-subtitle2 text-center"
                            )
    with ui.tabs().classes("w-full") as tabs:
        one = ui.tab("Source 1")
        two = ui.tab("Source 2")
    with ui.tab_panels(tabs, value=two).classes("w-full"):
        with ui.tab_panel(one):
            ui.html(
                f"""<iframe 
            src="https://vidsrc.to/embed/movie/{movie_details["imdb_id"]}"
            frameborder="0"
            allowfullscreen
            scrolling="no"
            class="w-[98vw] h-[90vh]"
            ></iframe>"""
            )
        with ui.tab_panel(two):
            ui.html(
                f"""<iframe 
            src="https://vidsrc.xyz/embed/movie/{movie_details["imdb_id"]}"
            frameborder="0"
            allowfullscreen
            scrolling="no"
            class="w-[98vw] h-[90vh]"
            ></iframe>"""
            )


@ui.page("/watch_tvshows")
async def watch_tvshows(tmdb_id):
    nav_bar.init_navbar()
    shows_details = await tmdb_api.get_show_details(tmdb_id)

    ui.image(shows_details["banner"]).classes("h-80")
    with ui.grid(columns=3):
        ui.image(shows_details["poster"]).props("fit=scale-down").classes("w-[25vw]")
        with ui.column():
            ui.label(shows_details["title"]).classes("text-h5")
            ui.label("Description:").classes("text-h6")
            ui.label(shows_details["plot"])
            ui.label("Casts:").classes("text-h6")
            with ui.scroll_area().classes("w-[30vw]"):
                with ui.row():
                    for cast in shows_details["casts"]:
                        with ui.image(cast["photo"]).classes("w-[8vw]"):
                            ui.label(cast["name"]).classes(
                                "absolute-bottom text-subtitle2 text-center"
                            )
    with ui.tabs().classes("w-full") as tabs:
        one = ui.tab("Source 1")
        two = ui.tab("Source 2")
    with ui.tab_panels(tabs, value=two).classes("w-full"):
        with ui.tab_panel(one):
            ui.html(
                f"""<iframe 
            src="https://vidsrc.to/embed/tv/{shows_details["imdb_id"]}"
            frameborder="0"
            allowfullscreen
            scrolling="no"
            class="w-[98vw] h-[90vh]"
            ></iframe>"""
            )
        with ui.tab_panel(two):
            ui.html(
                f"""<iframe 
            src="https://vidsrc.xyz/embed/tv/{shows_details["imdb_id"]}"
            frameborder="0"
            allowfullscreen
            scrolling="no"
            class="w-[98vw] h-[90vh]"
            ></iframe>"""
            )


@ui.page("/search")
async def search(mode, query):
    nav_bar.init_navbar()
    with ui.row():
        query_ = ui.input(label="Search").props("rounded outlined dense size=100")
        ui.button(
            icon="search",
            text="Search",
            on_click=lambda x: ui.open(f"/search?mode={mode}&query={query_.value}"),
        )
    items = await tmdb_api.search(mode=mode, query=query)
    ui.label(f"Search Results For: {query}")

    with ui.grid(columns=6):
        for item in items:
            item_card.item_card(
                title=item["title"],
                poster=item["poster"],
                href=item["id"],
                release_date=item["release_date"],
                ratings=item["ratings"],
                mode=mode,
            )


ui.run(port=5000)
