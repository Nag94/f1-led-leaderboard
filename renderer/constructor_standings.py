import time
from typing import List, Tuple
from rgbmatrix.graphics import DrawText, DrawLine
from renderer.renderer import Renderer
from data.color import Color
from utils import load_font, align_text_center, align_text_right


class ConstructorStandings(Renderer):
    """
    Render constructor standings

    Arguments:
        data (data.Data):                               Data instance

    Attributes:
        standings (List[ConstructorStandingsItem]):     Constructor standings list
        bg_color (rgbmatrix.graphics.Color):            Background color
        text_color (rgbmatrix.graphics.Font):           Text color
        font (rgbmatrix.graphics.Font):                 Font instance
        offset (int):                                   Row y-coord offset
        coords (dict):                                  Coordinates dictionary
        header_x (int):                                 Table header's x-coord
        header_y (int):                                 Table header's y-coord
        name_x (int):                                   Constructor's name x-coord
        name_y (int):                                   Constructor's name y-coord
        points_x (int):                                 Constructor's points x-coord
        points_y (int):                                 Constructor's points y-coord
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

        self.standings = self.data.constructor_standings

        self.bg_color = Color.GRAY.value  # Table header's bg color
        self.text_color = Color.WHITE.value  # Table header's text color

        self.font = load_font(self.data.config.layout['fonts']['tom_thumb'])

        self.offset = self.font.height + 2

        self.coords = self.data.config.layout['coords']['standings']
        self.header_x = align_text_center('Constructors',
                                          canvas_width=self.canvas.width,
                                          font_width=self.font.baseline - 1)[0]
        self.header_y = self.coords['header']['y']
        self.name_x = self.coords['name']['x']
        self.name_y = self.coords['name']['y']
        self.points_x = self.coords['points']['x']
        self.points_y = self.coords['points']['y']

    def render(self):
        self.canvas.Clear()

        self.render_header()

        pages = [(0, 3),  # No.1 - 3
                 (3, 7),  # No.4 - 7
                 (7, len(self.standings))]  # No.8 - 10

        for page in pages:
            self.render_page(page)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_header(self):
        for x in range(self.canvas.width):
            DrawLine(self.canvas, x, self.header_y - self.font.height, x, self.header_y, self.bg_color)
        DrawText(self.canvas, self.font, self.header_x, self.header_y, self.text_color, 'Constructors')

    def render_page(self, page: Tuple[int, int]):
        for i in range(page[0], page[1]):
            self.render_row(i)
        time.sleep(5.0)

        self.name_y = self.points_y = self.header_y  # Reset to top
        self.canvas.Clear()

    def render_row(self, i: int):
        self.bg_color = self.standings[i].constructor.colors[0]
        self.text_color = self.standings[i].constructor.colors[1]

        self.render_background()
        self.render_name(self.standings[i].constructor.name)
        self.render_points(self.standings[i].points)

        self.name_y += self.offset
        self.points_y += self.offset

    def render_background(self):
        for x in range(self.canvas.width):
            DrawLine(self.canvas, x, self.name_y - self.font.height, x, self.name_y, self.bg_color)

    def render_name(self, name: str):
        DrawText(self.canvas, self.font, self.name_x, self.name_y, self.text_color, name)

    def render_points(self, points: str):
        self.points_x = align_text_right(points, self.canvas.width, self.font.baseline - 1)
        DrawText(self.canvas, self.font, self.points_x, self.points_y, self.text_color, points)