
import numpy as np


class Buffer:
    def __init__(self):
        self.data = []
        self.height = -1
        self.width = -1

    def segment(self, type, origin, forward, right):

        # Type 0 is flat
        if type == 0:
            a = origin + forward
            self.data.append("L {} {}".format(*a))
            return

        # Odd types are female
        if type % 2 == 0:
            right = -right

        # Choose scale
        index = (type - 1) // 2
        unit = [0.35, 0.25][index]

        # Control points
        k = np.sqrt(2)
        a = origin + forward * (0.5 - 0.4 * unit)
        b = origin + forward * (0.5 - 0.4 / k * unit) + right * (0.6 * unit - 0.4 / k * unit)
        c = origin + forward * (0.5 + 0.4 / k * unit) + right * (0.6 * unit - 0.4 / k * unit)
        d = origin + forward * (0.5 + 0.4 * unit)
        e = origin + forward

        # Radii
        r1 = 0.2 * unit
        r2 = 0.4 * unit

        # Which side to choose
        cross = forward[0] * right[1] - forward[1] * right[0]
        is_system_mirrored = cross < 0
        if is_system_mirrored:
            sweep = 0
        else:
            sweep = 1

        # Draw hook
        self.data.append("L {} {}".format(*a))
        self.data.append("A {} {} 0 0 {} {} {}".format(r1, r1, sweep, *b))
        self.data.append("A {} {} 0 1 {} {} {}".format(r2, r2, 1 - sweep, *c))
        self.data.append("A {} {} 0 0 {} {} {}".format(r1, r1, sweep, *d))
        self.data.append("L {} {}".format(*e))

    def trace(self, types, origin, forward, right):
        # Note: type belongs to the piece on the right!
        self.data.append("M {} {}".format(*origin))
        for i, t in enumerate(types):
            self.segment(t, origin + i * forward, forward, right)

    def mirror_types(self, types):
        result = []
        for t in types:
            if t > 0:
                if t % 2 == 1:
                    t += 1
                else:
                    t -= 1
            result.append(t)
        return result

    def jigsaw(self, matrix):
        ex = np.array([1.0, 0.0])
        ey = np.array([0.0, 1.0])
        height, width, _ = matrix.shape
        self.height = height
        self.width = width

        # Draw horizontal lines
        for y in range(height):
            self.trace(matrix[y, :, 1], (0, y), ex, ey)
        self.trace(self.mirror_types(matrix[-1, :, 3]), (0, height), ex, ey)

        # Draw vertical lines
        for x in range(width):
            self.trace(matrix[:, x, 2], (x, 0), ey, ex)
        self.trace(self.mirror_types(matrix[:, -1, 0]), (width, 0), ey, ex)

    def save(self, file):
        data = " ".join(self.data)
        path = f'<path d="{data}"/>'
        scale = 64
        transform = f"scale({scale}) translate(0.5 0.5)"
        group = f'<g fill="none" stroke="red" stroke-width="{1 / scale}" transform="{transform}">{path}</g>'
        height = (self.height + 1) * scale
        width = (self.width + 1) * scale
        content = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">{group}</svg>'
        file.write(content)


matrix = [
    [[1, 0, 0, 1], [1, 0, 2, 1], [0, 0, 2, 1]],
    [[1, 2, 0, 1], [1, 2, 2, 2], [0, 2, 2, 2]],
    [[2, 2, 0, 0], [1, 1, 1, 2], [0, 1, 2, 0]],
]

matrix = np.array(matrix)

buffer = Buffer()
buffer.jigsaw(matrix)

with open("jigsaw.svg", "w") as file:
    buffer.save(file)