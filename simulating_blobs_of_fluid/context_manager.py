# pylint: disable=E1101
import cairo


class ContextManager:
    def __init__(self):
        self.set_resolution()
        self.create_surface()
        self.set_background()

    def set_resolution(self, width=600, height=600, scale=4):
        self.scale = scale
        self.width = width
        self.height = height

        return self

    def create_surface(self):
        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            self.width * self.scale,
            self.height * self.scale
        )
        self.surface.set_device_scale(self.scale, self.scale)
        self.ctx = cairo.Context(self.surface)

        return self

    def set_background(self, r=1, g=1, b=1):
        if isinstance(r, tuple):
            r, g, b, _ = r
        self.set_source_rgb(r, g, b)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

        return self

    def save(self, name='output.png'):
        self.surface.flush()
        self.surface.write_to_png(name)

    def set_source_rgb(self, r=1, g=1, b=1, a=1):
        self.ctx.set_source_rgba(r, g, b, a)
