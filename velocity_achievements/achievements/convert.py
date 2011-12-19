import cairo
import rsvg
import StringIO

def svg_to_png(svg_content, target_width, target_height):
    svg = rsvg.Handle(data=svg_content)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, target_width, target_height)
    context = cairo.Context(surface)
    context.scale(float(target_width)/svg.props.width, \
                float(target_height)/svg.props.height)
    svg.render_cairo(context)
    output = StringIO.StringIO()
    surface.write_to_png(output)
    return output.getvalue()
