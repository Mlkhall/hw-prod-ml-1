from doctest import debug

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from dash_bootstrap_templates import load_figure_template

from src.constants import TIME_INTERVAL

load_figure_template("dark")

# Путь к CSV файлу
CSV_FILE_PATH = 'logs/metric_log.csv'

# Инициализация Dash приложения
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Гистограмма Ошибок в Реальном Времени"

# Макет приложения
app.layout = dbc.Container([
        html.Div([
        html.H1("Гистограмма Абсолютных Ошибок"),
        dcc.Graph(id='error-histogram'),
        dcc.Interval(
            id='interval-component',
            interval=TIME_INTERVAL * 1000,  # обновление каждые TIME_INTERVAL секунд (TIME_INTERVAL * 1000 миллисекунд)
            n_intervals=0
        )
    ])
])


# Callback для обновления графика
@app.callback(
    Output('error-histogram', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_histogram(n):
    try:
        # Чтение данных из CSV файла
        df = pd.read_csv(CSV_FILE_PATH)

        # Создание гистограммы с использованием Plotly Express
        fig = px.histogram(
            df,
            x='absolute_error',
            nbins=30,  # количество бинов в гистограмме
            title='Распределение Абсолютных Ошибок',
            labels={'absolute_error': 'Абсолютная Ошибка'},
            opacity=0.75
        )

        # Обновление оформления
        fig.update_layout(
            xaxis_title="Абсолютная Ошибка",
            yaxis_title="Количество",
            template="plotly_dark"
        )
        fig.write_image("logs/error_distribution.png")
        return fig

    except Exception as e:
        # В случае ошибки, вернуть пустой график с сообщением
        return {
            "data": [],
            "layout": {
                "title": f"Ошибка при чтении данных: {e}"
            }
        }


if __name__ == '__main__':
    app.run_server(port=8050, host='0.0.0.0', debug=True)
