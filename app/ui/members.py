from shiny import ui, render, reactive
from app.db.session import SessionLocal
from app.services.member_service import MemberService

import pandas as pd


def members_ui():
    return ui.page_fluid(
        ui.h2("👥 Miembros"),

        # Filtros
        ui.card(
            ui.layout_columns(
                ui.card(
                    ui.input_action_button(
                        "btn_new_member",
                        "Nuevo usuario"
                    )
                ),
                ui.card(
                    # Futuro boton supongo
                ),
                col_widths=[3, 3]
            )
        ),

        ui.hr(),
        # Tabla principal
        ui.card(
            ui.h4("Listado de miembros"),
            ui.layout_column_wrap(
                ui.card(
                    ui.input_select(
                        "member_status",
                        "Status",
                        {
                            "all": "Todos",
                            "active": "Activos",
                            "inactive": "Inactivos"
                        },
                        selected="all"
                    )
                ),
                ui.card(    
                    ui.input_text(
                        "member_search",
                        "Buscar miembro...",
                        placeholder="nombre/email"
                    )
                ), 
            ),   
        ),
        ui.card(
            ui.output_data_frame("members_table"),
            full_screen=True
        )    
    )


def members_server(input, output, session):
    db = SessionLocal()
    # Definir la pantalla modal
    members_refresh = reactive.Value(0)
    def new_member_modal():
        return ui.modal(
            ui.h4("Nuevo miembro"),

            ui.input_text("full_name", "Nombre completo"),
            ui.input_text("email", "Email"),

            ui.input_checkbox(
                "is_admin",
                "Miembro administrador",
                value=False
            ),

            ui.input_checkbox(
                "is_active_member",
                "Miembro activo",
                value=True
            ),

            footer=ui.div(
                ui.input_action_button(
                    "confirm_new_member",
                    "Guardar",
                    class_="btn-success"
                ),
                ui.modal_button("Cancelar")
            )
        )
    
    @reactive.effect
    @reactive.event(input.btn_new_member)
    def open_new_member_modal():
        ui.modal_show(new_member_modal())

    @reactive.effect
    @reactive.event(input.confirm_new_member)
    def handle_create_member():
        full_name = input.full_name().strip()
        email = input.email().strip().lower()
        is_admin = input.is_admin()
        is_active = input.is_active_member()

        # Validaciones
        if not full_name:
            ui.notification_show("El nombre es obligatorio", type="error")
            return

        if not email or "@" not in email:
            ui.notification_show("Email inválido", type="error")
            return

        try:
            MemberService.create_member(
                db=db,
                full_name=full_name,
                email=email,
                is_admin=is_admin,
                is_active=is_active
            )

            ui.notification_show(
                "Miembro creado correctamente",
                type="message"
            )

            ui.modal_remove()

            # 🔁 Forzar refresco de la tabla
            members_refresh.set(members_refresh.get() + 1)

        except ValueError as e:
            ui.notification_show(str(e), type="error")
        

    @render.data_frame
    def members_table():
        members_refresh.get()  # ← dependencia reactiva
        
        data = MemberService.list_members(
            db,
            status=input.member_status(),
            keyword=input.member_search() 
        )

        df = pd.DataFrame(data)

        if df.empty:
            return df

        # Limpieza visual
        # hay q cambiar el is_active para personas, será mas sencillo al final
        df["is_admin"] = df["is_admin"].map({True: "Sí", False: "No"})
        df["is_member"] = df["is_member"].map({True: "Sí", False: "No"})
        df["person_active"] = df["person_active"].map({True: "Sí", False: "No"})
        df["total_contributed"] = df["total_contributed"].astype(float).round(2)

        df = df[[
            "full_name",
            "email",
            "is_admin",
            "is_member",
            "person_active",
            "total_contributed"
        ]]

        df.columns = [
            "Nombre",
            "Email",
            "admin",
            "Miembro",
            "Activo",
            "Total aportado (€)"
        ]

        return render.DataGrid(df)
