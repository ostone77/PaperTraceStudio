import os


def save_dxf(points, filename):

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as f:

        f.write("0\n")
        f.write("SECTION\n")
        f.write("2\n")
        f.write("ENTITIES\n")

        f.write("0\n")
        f.write("LWPOLYLINE\n")

        f.write("8\n")
        f.write("0\n")

        f.write("90\n")
        f.write(f"{len(points)}\n")

        f.write("70\n")
        f.write("1\n")      # Closed Polyline

        for x, y in points:

            f.write("10\n")
            f.write(f"{x:.3f}\n")

            f.write("20\n")
            f.write(f"{-y:.3f}\n")

        f.write("0\n")
        f.write("ENDSEC\n")

        f.write("0\n")
        f.write("EOF\n")