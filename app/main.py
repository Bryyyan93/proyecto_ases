from shiny import App, reactive, ui, render
from app.ui.login import login_ui, login_server
from app.ui.layout import main_layout, server_layout
from app.ui.dashboard import dashboard_server
from app.ui.members import members_server


def app_ui(request):
    return ui.output_ui("root")


def server(input, output, session):
    user_state = reactive.Value(None)

    login_server(input, output, session, user_state)

    @output
    @render.ui
    def root():
        # if user_state.get() is None:
        #    return login_ui()
        dashboard_server(input, output, session)
        server_layout(input, output, session)
        members_server(input, output, session)
        return main_layout()


app = App(app_ui, server)
