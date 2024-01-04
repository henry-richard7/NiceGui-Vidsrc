from nicegui import ui


def init_navbar():
    with ui.header().classes("items-center justify-between"):
        ui.label("Vidsrc").classes("text-h5")
        with ui.row():
            ui.button(
                "Moves", icon="movies", on_click=lambda x: ui.open("/?page_no=1")
            ).props("flat color=white")
            ui.button(
                "TV Shows", icon="tv", on_click=lambda x: ui.open("/shows?page_no=1")
            ).props("flat color=white")
