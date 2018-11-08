import os
import sys

import numpy as np
import svgwrite


dir_path = os.path.dirname(os.path.realpath(__file__))
root = dir_path.split('/')
index = root.index('web')
sys.path.append('/'.join(root[0:index]) + '/ConDep')

from condep.parsing.cd_definitions import CDDefinition
from condep.primitives import Primitives

try:
    from . import file_utils
except ImportError:
    import file_utils


class SVGService:

    FONT_SIZE = 20

    @staticmethod
    def diagram_exists(verb: str):
        static_root = file_utils._get_static_folder()

        filename = static_root + '/cd-diagrams/' + verb + ".svg"

        return os.path.isfile(filename)

    @staticmethod
    def create_diagram(verb: str, cd: CDDefinition):

        static_root = file_utils._get_static_folder()

        try:
            os.mkdir(static_root + '/cd-diagrams')
        except FileExistsError:
            pass

        svg_document = svgwrite.Drawing(
            filename=static_root + '/cd-diagrams/' + verb + ".svg",
            size=("200px", f"{SVGService.FONT_SIZE*2}px"))

        svg_document.attribs['font-size'] = SVGService.FONT_SIZE

        svg_document.add_stylesheet('svg-style.css', 'main')

        arrow_y_pos = SVGService.FONT_SIZE/2 + 2

        # Write subject
        actor_text = svg_document.text("Subject",
                                       insert=(0, SVGService.FONT_SIZE))

        svg_document.add(actor_text)

        actor_width = SVGService.text_width("Subject", SVGService.FONT_SIZE)

        # Add double arrow
        arrow_length = 60

        SVGService._add_double_arrow(
            svg_document, (actor_width+arrow_length+3, arrow_y_pos), (actor_width + 3, arrow_y_pos))

        # Write Primitive
        prim_text = svg_document.text(cd.primitive.name,
                                      insert=(actor_width + arrow_length + 6, SVGService.FONT_SIZE))

        svg_document.add(prim_text)

        prim_width = SVGService.text_width(
            cd.primitive.name, SVGService.FONT_SIZE)

        # Draw obj arrow
        obj_end_x = actor_width + arrow_length + prim_width + 10
        obj_start_x = obj_end_x + arrow_length
        SVGService._add_arrow(
            svg_document,
            (obj_start_x, arrow_y_pos),
            (obj_end_x, arrow_y_pos),
            'O'
        )

        # Add Obj Text
        obj_text = svg_document.text('Object',
                                     insert=(obj_start_x + 2, SVGService.FONT_SIZE))

        svg_document.add(obj_text)

        obj_width = SVGService.text_width('Object', SVGService.FONT_SIZE)

        # Set final size of the canvas, then save
        svg_document.attribs['width'] = f'{obj_start_x + obj_width + 3}px'
        svg_document.save()

    @staticmethod
    def _add_arrow(svg_document, start: tuple, end: tuple, label: str = None):
        if label:
            label_width = SVGService.text_width(label, SVGService.FONT_SIZE)
            label_x_pos = start[0] + (end[0] - start[0])/2 - label_width/2
            label_text = svg_document.text(label,
                                           insert=(label_x_pos, start[1] + SVGService.FONT_SIZE + 2))

            svg_document.add(label_text)

        svg_document.add(svg_document.line(start=start,
                                           end=end,
                                           stroke_width="1",))

        start_vec = np.array(start)
        end_vec = np.array(end)
        arrow_direction_vector = end_vec - start_vec

        magnitude = np.linalg.norm(arrow_direction_vector)

        unit_vec = arrow_direction_vector/magnitude

        norm = SVGService.perp_vector(unit_vec)

        triangle_points = [
            end_vec + 5*norm,
            end_vec - 5*norm,
            end_vec + 10*unit_vec]

        svg_document.add(svg_document.polygon(
            triangle_points,
            stroke_width="1",
            stroke="black",))

    @staticmethod
    def _add_double_arrow(svg_document, start: tuple, end: tuple):

        start_vec = np.array(start)
        end_vec = np.array(end)
        arrow_direction_vector = end_vec - start_vec

        magnitude = np.linalg.norm(arrow_direction_vector)

        unit_vec = arrow_direction_vector/magnitude

        # remove length of arrow
        start_vec = start_vec + 10*unit_vec
        end_vec = end_vec - 10*unit_vec

        norm = SVGService.perp_vector(unit_vec)

        svg_document.add(svg_document.line(start=start_vec + 3*norm,
                                           end=end_vec + 3*norm,
                                           stroke_width="1",
                                           stroke="black",))

        svg_document.add(svg_document.line(start=start_vec - 3*norm,
                                           end=end_vec - 3*norm,
                                           stroke_width="1",
                                           stroke="black",))

        triangle_points = [
            end_vec + 5*norm,
            end_vec - 5*norm,
            end_vec + 10*unit_vec
        ]

        svg_document.add(svg_document.polygon(
            triangle_points,
            stroke_width="1",
            stroke="black")
        )

        triangle_points2 = [
            start_vec + 5*norm,
            start_vec - 5*norm,
            start_vec - 10*unit_vec]

        svg_document.add(svg_document.polygon(
            triangle_points2,
            stroke_width="1",
            stroke="black",))

    @staticmethod
    def perp_vector(vec: np.array):
        return np.array([vec[1], -vec[0]])

    @staticmethod
    def text_width(text: str, fontsize: int):
        # https://stackoverflow.com/questions/24337531/how-to-determine-text-width-and-height-when-using-svgwrite-for-python#46673288

        try:
            import cairo
        except Exception:
            print('Cario not installed- estimating text width', file=sys.stderr)
            return 0.7 * len(text) * fontsize
        surface = cairo.SVGSurface('undefined.svg', 1280, 200)
        cr = cairo.Context(surface)
        cr.select_font_face('Arial', cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(fontsize)
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(
            text)
        return width


if __name__ == '__main__':
    cd = CDDefinition(Primitives.EXPEL)
    maker = SVGService()
    maker.create_diagram('test', cd)
