import os
import sys

import numpy as np
import svgwrite


dir_path = os.path.dirname(os.path.realpath(__file__))
root = dir_path.split('/')
index = root.index('web')
sys.path.append('/'.join(root[0:index]) + '/ConDep')

from condep.parsing.cd_definitions import CDDefinition, CDDefinitionPredecessorWrapper
from condep.primitives import Primitives

try:
    from . import file_utils
except ImportError:
    import file_utils


class SVGService:

    FONT_SIZE = 20
    ARROW_LENGTH = 30
    GAP_BETWEEN_LEVELS = 60

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

        if cd.preceding:
            doc_height = SVGService.FONT_SIZE*2 + 100
        else:
            doc_height = SVGService.FONT_SIZE*2

        svg_document = svgwrite.Drawing(
            filename=static_root + '/cd-diagrams/' + verb + ".svg",
            size=("200px", f"{doc_height}px"))

        svg_document.attribs['font-size'] = SVGService.FONT_SIZE

        svg_document.add_stylesheet('svg-style.css', 'main')

        num_levels = 0
        fuse = 0
        current_event = cd
        while True:
            if fuse > 100:
                raise RuntimeError

            num_levels += 1
            if current_event.preceding:
                current_event = current_event.preceding.definition
            else:
                break

        first_event_offset = (
            num_levels-1) * (SVGService.FONT_SIZE + SVGService.GAP_BETWEEN_LEVELS)
        obj_start_x, obj_width, actor_width = SVGService._draw_event(
            cd, svg_document, first_event_offset)
        doc_width = obj_start_x + obj_width

        if cd.preceding:
            obj_start_x_pre, obj_width_pre, actor_width_pre = SVGService._draw_event(
                cd.preceding.definition, svg_document, 0)

            if obj_start_x_pre + obj_width_pre > doc_width:
                doc_width = obj_start_x_pre + obj_width_pre

            # Draw obj arrow
            arrow_x = actor_width + SVGService.ARROW_LENGTH
            SVGService._add_arrow(
                svg_document,
                (arrow_x, SVGService.FONT_SIZE + 5),
                (arrow_x, SVGService.FONT_SIZE +
                 SVGService.GAP_BETWEEN_LEVELS - 10),
                'r'
            )

        # Set final size of the canvas, then save
        svg_document.attribs['width'] = f'{doc_width + 3}px'
        svg_document.save()

    # PRIVATE METHODS

    @staticmethod
    def _draw_event(cd: CDDefinition, svg_document, y_offset: int = 0):
        arrow_y_pos = SVGService.FONT_SIZE/2 + 2 + y_offset

        # Write subject
        actor_label = cd.actor_override or "Subject"
        actor_text = svg_document.text(actor_label,
                                       insert=(0, SVGService.FONT_SIZE + y_offset))

        svg_document.add(actor_text)

        actor_width = SVGService._text_width(actor_label, SVGService.FONT_SIZE)

        # Add double arrow
        arrow_length = 60

        SVGService._add_double_arrow(
            svg_document, 
            (actor_width+arrow_length+3, arrow_y_pos), 
            (actor_width + 3, arrow_y_pos)
        )

        # Write Primitive
        prim_text = svg_document.text(cd.primitive.name,
                                      insert=(actor_width + arrow_length + 6, SVGService.FONT_SIZE + y_offset))

        svg_document.add(prim_text)

        prim_width = SVGService._text_width(
            cd.primitive.name, SVGService.FONT_SIZE)

        # Draw obj arrow
        obj_end_x = actor_width + arrow_length + prim_width + 20
        obj_start_x = obj_end_x + arrow_length
        SVGService._add_arrow(
            svg_document,
            (obj_start_x, arrow_y_pos),
            (obj_end_x, arrow_y_pos),
            'O'
        )

        # Add Obj Text
        obj_name = cd.object_override or 'Object'
        obj_text = svg_document.text(obj_name,
                                     insert=(obj_start_x + 3, SVGService.FONT_SIZE + y_offset))

        svg_document.add(obj_text)

        obj_width = SVGService._text_width(obj_name, SVGService.FONT_SIZE)

        return obj_start_x, obj_width, actor_width

    @staticmethod
    def _add_arrow(svg_document, start: tuple, end: tuple, label: str = None):
        if label:
            if start[0] != end[0]:
                label_width = SVGService._text_width(
                    label, SVGService.FONT_SIZE)
                label_x_pos = start[0] + (end[0] - start[0])/2 - label_width/2
                label_text = svg_document.text(label,
                                               insert=(label_x_pos, start[1] + SVGService.FONT_SIZE + 2))

                svg_document.add(label_text)
            elif start[1] != end[1]:
                label_y_pos = start[1] + \
                    (end[1] - start[1])/2 + SVGService.FONT_SIZE/2
                label_text = svg_document.text(label,
                                               insert=(start[0] + SVGService.FONT_SIZE + 2, label_y_pos))

                svg_document.add(label_text)
            else:
                raise NotImplementedError('Diagonal lines not supported')

        svg_document.add(svg_document.line(start=start,
                                           end=end,
                                           stroke_width="1",))

        start_vec = np.array(start)
        end_vec = np.array(end)
        arrow_direction_vector = end_vec - start_vec

        magnitude = np.linalg.norm(arrow_direction_vector)

        unit_vec = arrow_direction_vector/magnitude

        norm = SVGService._perp_vector(unit_vec)

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

        norm = SVGService._perp_vector(unit_vec)

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
    def _perp_vector(vec: np.array):
        return np.array([vec[1], -vec[0]])

    @staticmethod
    def _text_width(text: str, fontsize: int):
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
    cd = CDDefinition(Primitives.MOVE)

    cd.preceding = CDDefinitionPredecessorWrapper()

    cd.preceding.definition = CDDefinition(Primitives.PTRANS)

    maker = SVGService()
    maker.create_diagram('test', cd)
