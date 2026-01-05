from shiny import ui, reactive
from app.services.auth_service import AuthService
from app.db.session import SessionLocal


def login_ui():
    return ui.page_fluid(
        ui.input_text("username", "Usuario"),
        ui.input_password("password", "Contraseña"),
        ui.input_action_button("login", "Entrar"),
        ui.output_text("login_error"),
    )


def login_server(input, output, session, user_state):

    @reactive.Effect
    @reactive.event(input.login)
    def do_login():
        db = SessionLocal()
        user = AuthService.authenticate(
            db,
            input.username(),
            input.password()
        )
        print("USER FROM DB:", user)

        if not user:
            user_state.set(None)
            return

        user_state.set(user)
