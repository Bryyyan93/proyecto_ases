from shiny import ui, render
from app.db.session import SessionLocal
from app.services.dashboard_service import DashboardService
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def dashboard_ui():
    return ui.page_fluid(
        ui.h1("📊 Dashboard"),
        ui.hr(),
        # KPIs arriba
        ui.layout_columns(
            ui.card(
                ui.h4("Usuarios"),
                ui.output_text("users_count")
            ),
            ui.card(
                ui.h4("Miembros"),
                ui.output_text("members_count")
            ),
            ui.card(
                ui.h4("Proyectos"),
                ui.output_text("projects_count")
            ),
            col_widths=[4, 4, 4]
        ),

        # Zona de datos
        ui.hr(),
        ui.layout_columns(
            ui.card(
                ui.h4("📈 Evolución de ingresos"),
                ui.input_date_range(
                    id="date_range",
                    label="Periodo",
                    start=date(2025, 1, 1),
                    end=date.today(),
                    format="dd/mm/yyyy",
                    autoclose=True
                ),
                ui.output_plot("monthly_income_chart"),
                full_screen=True
            )
        )
    )


def dashboard_server(input, output, session):

    db = SessionLocal()
    summary = DashboardService.summary(db)
    # projects = DashboardService.projects_by_status(db)
    # activity = DashboardService.recent_activity(db)

    # Dashboard. muestra un resumen de los proyectos, miembres y usuarios
    @output
    @render.text
    def users_count():
        return str(summary["users_count"])

    @output
    @render.text
    def members_count():
        return str(summary["members_count"])

    @output
    @render.text
    def projects_count():
        return str(summary["projects_count"])

    # Grafico de los ingresos mensuales
    @output
    @render.plot
    def monthly_income_chart():
        start_date, end_date = input.date_range()
        # Llamamos al backend
        data = DashboardService.monthly_financials(
            db,
            start_date=start_date,
            end_date=end_date
        )
        df = pd.DataFrame(data)  # Convertimos a DataFrame

        # Crear figura explícita
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots(figsize=(8, 4))

        # Caso sin datos
        if df.empty:
            ax.text(0.5, 0.5, "No hay datos",
                    ha="center", va="center")
            ax.axis("off")
            return fig

        # convertir los valores a tipos numéricos
        df["real_amount"] = df["real_amount"].astype(float)
        df["expected_amount"] = df["expected_amount"].astype(float)
        df["month"] = pd.to_datetime(df["month"])

        # Linea ingresos realeas
        sns.lineplot(
            data=df,
            x="month",
            y="real_amount",
            label="Ingresos reales",
            marker="o",
            ax=ax
        )

        # Línea ingresos esperados
        sns.lineplot(
            data=df,
            x="month",
            y="expected_amount",
            linestyle="--",
            label="Ingresos esperados"
        )

        # Estética mínima
        ax.set_title("Ingresos mensuales")
        ax.set_xlabel("Mes")
        ax.set_ylabel("€")
        ax.legend()
        # ax.grid(True)
        fig.autofmt_xdate()

        return fig
