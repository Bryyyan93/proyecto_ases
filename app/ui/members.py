from shiny import ui, render
from app.db.session import SessionLocal
from app.services.member_service import MemberService

import pandas as pd


def members_ui():
    return ui.page_fluid(
        ui.h2("👥 Miembros"),

        # Filtros
        ui.card(
            ui.layout_columns(
                ui.input_select(
                    "member_status",
                    "Estado",
                    {
                        "all": "Todos",
                        "active": "Activos",
                        "inactive": "Inactivos"
                    },
                    selected="all"
                ),
                col_widths=[4]
            )
        ),

        ui.br(),

        # Tabla principal
        ui.card(
            ui.h4("Listado de miembros"),
            ui.output_data_frame("members_table"),
            full_screen=True
        )
    )


def members_server(input, output, session):

    db = SessionLocal()

    @render.data_frame
    def members_table():
        data = MemberService.list_members(
            db,
            status=input.member_status()
        )

        df = pd.DataFrame(data)

        if df.empty:
            return df

        # Limpieza visual
        df["is_user"] = df["is_user"].map({True: "Sí", False: "No"})
        df["is_member"] = df["is_member"].map({True: "Sí", False: "No"})
        df["total_contributed"] = df["total_contributed"].astype(float).round(2)

        df = df[[
            "full_name",
            "email",
            "is_user",
            "is_member",
            "total_contributed"
        ]]

        df.columns = [
            "Nombre",
            "Email",
            "Usuario",
            "Miembro",
            "Total aportado (€)"
        ]

        return render.DataGrid(df)
