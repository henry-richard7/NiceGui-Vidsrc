from nicegui import ui


def item_card(title: str, poster: str, href: str):
    with ui.card().tight():
        ui.image(poster)
        with ui.card_section():
            ui.label(title)
