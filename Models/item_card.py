from nicegui import ui


def item_card(
    title: str,
    poster: str,
    release_date: str,
    ratings: float,
    href: str,
    mode: str = "movie",
):
    with ui.card().tight():
        ui.image(poster)

        with ui.card_section():
            ui.label(title).classes("text-bold")
            with ui.row():
                ui.icon(name="star", size="18px")
                ui.label(ratings).classes("text-weight-light")

            ui.label(release_date).classes("text-weight-light")
            if mode == "movie":
                target_link = f"/watch_movie?tmdb_id={href}"
            else:
                target_link = f"/watch_tvshows?tmdb_id={href}"
            ui.button(
                icon="visibility",
                text="WATCH NOW",
                on_click=lambda x: ui.open(target_link),
            )
