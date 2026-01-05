from shiny import ui
from app.ui.dashboard import dashboard_ui


def main_layout():
    return ui.page_sidebar(
        ui.sidebar(
            ui.h4("Menú"),
            ui.navset_pill(
                ui.nav_panel("Dashboard"),
                ui.nav_panel("Miembros", "members"),
                ui.nav_panel("Proyectos", "projects"),
            ),
            width=250
        ),
        dashboard_ui(),
        ui.output_ui("content")
    )
