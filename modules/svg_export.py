import os


def save_svg(points, filename):

    if not points:
        return

    min_x = min(x for x, y in points)
    min_y = min(y for x, y in points)

    points = [

        (

            x - min_x,

            y - min_y

        )

        for x, y in points

    ]

    max_x = max(x for x, y in points)
    max_y = max(y for x, y in points)

    point_string = " ".join(

        f"{x},{y}"

        for x, y in points

    )

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>

<svg
xmlns="http://www.w3.org/2000/svg"
version="1.1"
width="{max_x}"
height="{max_y}"
viewBox="0 0 {max_x} {max_y}">

<polyline

points="{point_string}"

fill="none"

stroke="black"

stroke-width="1"/>

</svg>
'''

    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as f:

        f.write(svg)