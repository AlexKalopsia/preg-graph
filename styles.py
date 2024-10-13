from dataclasses import dataclass
from enum import Enum
from typing import List


class LineStyle(Enum):
    SOLID = '-'
    DASHED = '--'
    DOTTED = ':'
    DASHDOT = '-.'

@dataclass
class Color:
    hex: str
    alpha: float

@dataclass
class Line():
    color: Color
    width: float
    style: LineStyle

@dataclass
class Dot:
    color: Color
    size: float

@dataclass
class StyleParameters:
    background_color: str
    graph_background_color: str
    text_color: str
    line: Line
    dot: Dot
    grid_alpha: float
    trimesters_separator_alpha: float
    trimesters_color: List[Color]
    birth_separator: Line
    post_birth_color: Color

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
            line=Line(Color('#ffa500',1.0),2,LineStyle.DASHED),
            dot=Dot(Color('#0000ff',1.0),8),
            grid_alpha=0.2,
            trimesters_separator_alpha=0.65,
            trimesters_color=[Color('#fff', 1.0), 
                              Color('#fff', 1.0), 
                              Color('#fff', 1.0)],
            birth_separator=Line(Color('#ffa500',0.5),1,LineStyle.SOLID),
            post_birth_color=Color('#ffa500',0.035)
        )
    ),
    'dark': Style(
        name='Dark',
        params=StyleParameters(
            background_color='#0d1117',
            graph_background_color='#010409',
            text_color='#e8eff4',
            line=Line(Color('#b37a09',1.0),2,LineStyle.SOLID),
            dot=Dot(Color('#ffa500',1.0),10),
            grid_alpha=0.05,
            trimesters_separator_alpha=0.65,
            trimesters_color=[Color('#010409', 1.0), 
                              Color('#010409', 1.0), 
                              Color('#010409', 1.0)],
            birth_separator=Line(Color('#a9a9a9',0),2,LineStyle.SOLID),
            post_birth_color=Color('#010205',1.0)
        )
    )
}