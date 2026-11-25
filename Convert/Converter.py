from pdf_to_markdown import (
    ConverterBase,
    SuperChapter,
    DocumentWithSubChapters,
)


class Converter(ConverterBase):
    """
    Converter for Collecting Gold Dust book.

    The rules of the page headers (that the sanitizing removes) belong to the
    structural information of the book, see StructuralInfo.get_page_header.
    """

    # Lines of paragraphs longer than this are broken (markdownlint MD013),
    # without starting new paragraphs.
    DEFAULT_MAXIMUM_LINE_LENGTH = 800

    def __init__(self, pdf_filename, structural_info, maximum_line_length=None):
        if maximum_line_length is None:
            maximum_line_length = self.DEFAULT_MAXIMUM_LINE_LENGTH
        document = DocumentWithSubChapters(
            structural_info.book_title,
            publication_info=getattr(structural_info, "publication_info", None),
        )
        ConverterBase.__init__(
            self, pdf_filename, document, structural_info, maximum_line_length
        )

    def break_document_into_chapters(self):
        return ConverterBase.break_document_into_chapters(self, SuperChapter)
