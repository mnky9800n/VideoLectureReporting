import numpy as np

from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, Plot, Figure, Package
from pylatex.numpy import Matrix
from pylatex.utils import italic, escape_latex

class LatexReport:

    def _mkfig(self, Document, SectionName, FileName, FigCaption):
        #with doc.create(Section('Timeline Graph')):
        #    with doc.create(Figure(position='h!')) as timeline:
        #        timeline.add_image(image_dir + 'timeline.png', width='600px')
        #        timeline.add_caption('Georgia Tech has 15 week semesters with two week final periods.')

        image_dir = "C:/Users/Administrator/Google Drive/code learning/VideoLectureReporting/VideoLectureReporting/images/"

        with Document.create(Section(SectionName)):
            with Document.create(Figure(position='h!')) as timeline:
                timeline.add_image(image_dir + FileName, width='600px')
                timeline.add_caption(FigCaption)
    
    def Generate(self):
        
        doc = Document()
        doc.filename = 'Report'

        doc.packages.append(Package('geometry', options=['tmargin=1cm', 'lmargin=1cm']))
        
        self._mkfig(doc
              , 'Timeline Graph'
              , 'timeline.png'
              , 'Georgia Tech has 15 week semesters with two week final periods.')

        self._mkfig(doc
              , 'Fraction of Students Accessing'
              , 'fractionAccessing.png'
              , 'Not all students access videos.')

        self._mkfig(doc
              , 'Access Density'
              , 'fourbyfour.png'
              , 'Students generally access lab videos more than lecture videos.')

        self._mkfig(doc
              , 'Which Students Watch Which Videos?'
              , 'binarymap.png'
              , 'Most students skip at least some of the videos.')

        self._mkfig(doc
              , 'Semester Access Map'
              , 'heatmap.png'
              , 'Students generally access videos as they are assigned and do not return to videos later in the semester.')

        doc.generate_pdf()

if __name__ == "__main__":
    LR = LatexReport()
    LR.Generate()