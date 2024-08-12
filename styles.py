from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class StyleParameters:
    background_color: str
    graph_background_color: str
    text_color: str
    line_style: str
    line_color: str
    line_width: float
    dot_color: str
    dot_size: float
    trimesters_color: List[Tuple[str, float]] 
    trimesters_separator_alpha: float
    grid_alpha: float

@dataclass
class Style:
    name: str
    params: StyleParameters

styles = {
    'default': Style(
        name='Default',
        params=StyleParameters(
            background_color='#fff',
            graph_background_color='#fff',
            text_color='#000',
            line_style='--',
            line_color='#ffa500',
            line_width=2,
            dot_color='blue',
            dot_size=8,
            trimesters_color=[['#fff', 1.0], ['#fff', 1.0], ['#fff', 1.0]],
            trimesters_separator_alpha=0.65,
            grid_alpha=0.2
        )
    ),
    'dark': Style(
        name='Dark',
        params=StyleParameters(
            background_color='#0d1117',
            graph_background_color='#010409',
            text_color='#e8eff4',
            line_style='-',
            line_color='#b37a09',
            line_width=2,
            dot_color='#ffa500',
            dot_size=10,
            trimesters_color=[['#010409', 1.0], ['#010409', 1.0], ['#010409', 1.0]],
            trimesters_separator_alpha=0.65,
            grid_alpha=0.05
        )
    )
}