import numpy as np
import svgwrite

# from condep.parsing.cd_definitions import CDDefinition

class SVGMaker:

    def process(self):

        svg_document = svgwrite.Drawing(
            filename = "test-svgwrite.svg",
            size = ("200px", "150px"))


        self._add_double_arrow(svg_document, (30,10),(10,10))


        # svg_document.add(svg_document.text("Hello World",
        #                                 insert = (210, 110)))

        svg_document.save()

    
    def _add_arrow(self, svg_document, start:tuple, end:tuple):
        svg_document.add(svg_document.line(start=start,
                                            end=end,
                                        stroke_width = "1",
                                        stroke = "black",))

        start_vec = np.array(start)
        end_vec = np.array(end)
        arrow_direction_vector = end_vec - start_vec

        magnitude = np.linalg.norm(arrow_direction_vector)

        unit_vec = arrow_direction_vector/magnitude

        norm = self.perp_vector(unit_vec)

        triangle_points = [
            end_vec + 5*norm,
            end_vec - 5*norm,
            end_vec + 10*unit_vec ]

        svg_document.add(svg_document.polygon(
            triangle_points,
                                        stroke_width = "1",
                                        stroke = "black",))

    def _add_double_arrow(self, svg_document, start:tuple, end:tuple):
        

        start_vec = np.array(start)
        end_vec = np.array(end)
        arrow_direction_vector = end_vec - start_vec

        magnitude = np.linalg.norm(arrow_direction_vector)

        unit_vec = arrow_direction_vector/magnitude

        norm = self.perp_vector(unit_vec)

        svg_document.add(svg_document.line(start=start_vec + 3*norm,
                                            end=end_vec + 3*norm,
                                        stroke_width = "1",
                                        stroke = "black",))

        svg_document.add(svg_document.line(start=start_vec - 3*norm,
                                            end=end_vec - 3*norm,
                                        stroke_width = "1",
                                        stroke = "black",))

        triangle_points = [
            end_vec + 5*norm,
            end_vec - 5*norm,
            end_vec + 10*unit_vec ]

        svg_document.add(svg_document.polygon(
            triangle_points,
                                        stroke_width = "1",
                                        stroke = "black",))

        triangle_points2 = [
            start_vec + 5*norm,
            start_vec - 5*norm,
            start_vec - 10*unit_vec ]

        svg_document.add(svg_document.polygon(
            triangle_points2,
                                        stroke_width = "1",
                                        stroke = "black",))


    @staticmethod
    def perp_vector(vec:np.array):
        return np.array([vec[1], -vec[0]])

if __name__ == '__main__':
    maker = SVGMaker()
    maker.process()