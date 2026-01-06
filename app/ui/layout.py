# app/ui/layout.py
from shiny import ui, render
from app.ui.dashboard import dashboard_ui
from app.ui.members import members_ui


def main_layout():
    return ui.page_sidebar(
        ui.sidebar(
            ui.h4("Menú"),
            ui.navset_pill(
                ui.nav_panel("Dashboard", value="dashboard"),
                ui.nav_panel("Miembros", value="members"),
                ui.nav_panel("Proyectos", value="projects"),
                id="nav",
                selected="dashboard"
            ),
            width=250
        ),
        ui.output_ui("content")
    )


def server_layout(input, output, session):
    @output
    @render.ui
    def content():
        nav = input.nav() or "dashboard"
        match nav:
            case "dashboard":
                return dashboard_ui()
            case "members":
                return members_ui()
            case None:
                return dashboard_ui()
