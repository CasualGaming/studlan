# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from bs4 import BeautifulSoup

        # Settings for general layout
        rows = 5
        columns = 2
        seats_per_row = 10
        seats_per_column = 2

        # Settings for svg element
        svg_height = 1000
        svg_width = 1000
        svg_margin_left = 20
        svg_margin_top = 120
        svg_margin_adjacent = 2
        svg_column_separator_margin = 50
        svg_row_separator_margin = 30

        # Settings for seats
        seat_width = 30
        seat_width_px = '30px'
        seat_height = 20
        seat_height_px = '20px'
        seat_rx = '2px'
        seat_ry = '2px'

        # Initiate svg element
        soup = BeautifulSoup('<svg>', 'html.parser')
        soup.svg['height'] = svg_height
        soup.svg['width'] = svg_width

        # Build svg with elements
        current_y = svg_margin_top
        for column in range(0, columns):
            for __ in range(0, rows):
                for __ in range(0, seats_per_column):
                    current_x = svg_margin_left + (((seat_width * seats_per_row + svg_margin_adjacent) * (seats_per_row - 1)) + svg_column_separator_margin) * column
                    for __ in range(0, seats_per_row):
                        element_a = soup.new_tag('a')
                        element_rect = soup.new_tag('rect')
                        element_rect['height'] = seat_height_px
                        element_rect['width'] = seat_width_px
                        element_rect['rx'] = seat_rx
                        element_rect['ry'] = seat_ry
                        element_rect['x'] = current_x
                        element_rect['y'] = current_y
                        element_a.insert(1, element_rect)
                        soup.svg.insert(1, element_a)
                        current_x += svg_margin_adjacent + seat_width
                    current_y += svg_margin_adjacent + seat_height
                current_y += svg_row_separator_margin
            current_y = svg_margin_top
            current_x = svg_margin_left

        # Print debug
        # print(soup.prettify())

        # Print output to html file
        html = soup.prettify('utf-8')
        with open('output.html', 'wb') as out_file:
            out_file.write(html)
