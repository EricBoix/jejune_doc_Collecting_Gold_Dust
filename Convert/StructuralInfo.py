import roman

from pdf_to_markdown import (
    ChapterSplitter,
    ConverterError,
    MultiplePatternSplitter,
    NameLessSinglePatternSplitter,
    PublicationInfo,
    StructuralInfoBase,
)
from Sanitizer import Sanitizer


class StructuralInfo(StructuralInfoBase):
    publication_info = PublicationInfo(
        doc_name="collecting-gold-dust",
        author="Sayadaw U Tejaniya",
        isbn="978-0-9835844-2-4",
    )

    # The structural information per se with extension specifics
    # - "type" can be "illustration" (with an optional "header" boolean flag)
    # - a "chapter_info" can have an optional "illumination_delimiter"
    EXTRA_PAGE_INFO_KEYS = frozenset({"header"})

    class chapter_splitter(ChapterSplitter):
        """Chapter splitter for Collecting Gold Dust.

        Detects chapter boundaries based on:
        1. Static declarations in pages_info (type == "chapter")
        2. Exactly 6 newlines
        """

        def __init__(self, structural_info):
            structural_info = structural_info
            # The following regex stands for
            # (?<!(\n)): negative lookbehind for a newline (that is: make sure
            #            we start the match at the first newline occurrence)
            # (\n){6}: match six newlines (note: but they can be more than that
            #          standing afterwards. Hence, if we where to leave the
            #          regex like that, it could be that they are more newlines
            #          than 6.)
            # (?!(\n)): look-forward stating that when matching the above 6
            #          newlines the next character can NOT be a newline.
            # The whole regex thus states: match EXACTLY (no more, no less) 6
            # newlines.
            chapter_name_separator_regex = r"(?<!(\n))(\n){6}(?!(\n))"
            chapter_name_separator_first_occurrence = 100
            ChapterSplitter.__init__(
                self,
                structural_info,
                chapter_name_separator_regex,
                chapter_name_separator_regex,  # Extractor = Separator
                chapter_name_separator_first_occurrence,
            )

    # class superchapter_to_chapter_splitter(SinglePatternSplitter):
    class superchapter_to_chapter_splitter(MultiplePatternSplitter):
        def __init__(self):
            # Refer to comments of test class TestChapterRegex within
            # test_main.py for explanations
            # (The text of the pages is plain ASCII, see TextExtractor: a double quote
            # stands for the opening and the closing ones)
            chapter_name_characters = "[A-Z|?|'| \",]{3,100}"
            multi_lines_chapter_name = (
                r"(?:"
                + chapter_name_characters
                + r"\n(?! ))*"
                + chapter_name_characters
            )
            middle_page_subchapter_pattern = (
                r"\n\n\n" + multi_lines_chapter_name + r"\n"
            )
            top_page_subchapter_pattern = r"^" + multi_lines_chapter_name
            breaking_patterns = [  # Visual sugar
                middle_page_subchapter_pattern,
                top_page_subchapter_pattern,
            ]
            MultiplePatternSplitter.__init__(
                self,
                breaking_patterns,
                multi_lines_chapter_name,
            )

    class chapter_to_paragraph_splitter(NameLessSinglePatternSplitter):
        def __init__(self):
            breaking_pattern = "\n    "
            NameLessSinglePatternSplitter.__init__(self, breaking_pattern)

    @property
    def total_page_number(self) -> int:
        return 160

    def __init__(self):
        StructuralInfoBase.__init__(self)
        self._sanitizer = Sanitizer(self)
        # The original pdf document has a title that is depicted (as opposed to
        # written in text) in the cover illustration and thus cannot be
        # automatically extracted. This title ends-up embedded in some headers
        # and must thus be manually provided.
        self.book_title = "COLLECTING GOLD DUST: Nurturing the Dhamma in Daily Living"

        # The preamble section pages use roman numbering. This offsets the
        # numbering of the body pages
        self.page_numbering_offset = 16

        self._pages_info = {
            0: {"drop_page": True},  # Front cover
            1: {"drop_page": True},  # Book title
            2: {"drop_page": True},  # Illustration
            3: {
                # Chapters with no given name are artificial/fake chapters that
                # do not exist in the book. They are a technicality for the
                # first pages not to be devoid of a belonging chapter:
                "type": "chapter",
                "chapter_info": {
                    "name": "Introduction (ghost chapter)",
                    "illumination_delimiter": None,
                },
            },
            4: {"drop_page": True},
            5: {
                # They are two reasons for which we don't have to look for
                # a paragraph continuation on the next page:
                # 1. because the page ends a chapter (and hence the paragraph
                #    has to be finished)
                # 2. It just so happens that the paragraph ends up nicely at
                #    the bottom of this page.
                # Here we encountered the first case
                "paragraph_fits_on_page": True,
            },
            # 6: implicit "generic"/default page
            7: {
                "chapter_info": {"illumination_delimiter": "MBhaddanta"},
                "paragraph_fits_on_page": True,  # This page ends the chapter
            },
            9: {"chapter_info": {"illumination_delimiter": "Iobservation"}},
            15: {"chapter_info": {"illumination_delimiter": "Wwords"}},
            16: {"paragraph_fits_on_page": True},  # This page ends the chapter
            17: {"drop_page": True},
            18: {"drop_page": True},
            19: {"drop_page": True},
            20: {
                # Although this illustration is decorated with text (or the other way round), the text content is an extracted quote
                # from the body of the chapter. We can thus drop it without
                # content loss.
                "drop_page": True,
            },
            21: {"chapter_info": {"illumination_delimiter": "Ytime"}},
            24: {"drop_page": True},  # Illustration with non meaningful text
            30: {"drop_page": True},  # Illustration with non meaningful text
            35: {"paragraph_fits_on_page": True},  # Paragraph nicely ended.
            36: {"drop_page": True},  # Illustration with non meaningful text
            37: {"paragraph_fits_on_page": True},
            39: {"paragraph_fits_on_page": True},
            41: {"paragraph_fits_on_page": True},  # This page ends the chapter
            42: {
                # This illustration has some additional textual content that
                # is original and that is not part of the main text.
                # We thus keep it.
                "type": "illustration",
            },
            43: {"chapter_info": {"illumination_delimiter": "WTwo"}},
            44: {"drop_page": True},  # Illustration with non meaningful text
            45: {"paragraph_fits_on_page": True},
            46: {"paragraph_fits_on_page": True},
            48: {"paragraph_fits_on_page": True},
            50: {"drop_page": True},  # Illustration with non meaningful text
            51: {"paragraph_fits_on_page": True},
            53: {"paragraph_fits_on_page": True},
            56: {"drop_page": True},  # Illustration with non meaningful text
            60: {"paragraph_fits_on_page": True},
            61: {
                "typo_and_fix": {  # PDF extraction artifact
                    "typo": "GET TING",
                    "fix": "GETTING",
                }
            },
            62: {"drop_page": True},  # Illustration with non meaningful text
            63: {"paragraph_fits_on_page": True},
            64: {"type": "illustration"},  # Illustration with valid text
            65: {"chapter_info": {"illumination_delimiter": "Man"}},
            67: {"paragraph_fits_on_page": True},
            68: {"drop_page": True},
            70: {"paragraph_fits_on_page": True},
            72: {"paragraph_fits_on_page": True},
            73: {"paragraph_fits_on_page": True},
            74: {"drop_page": True},
            76: {"paragraph_fits_on_page": True},
            77: {"drop_page": True},
            78: {"type": "illustration"},
            79: {"chapter_info": {"illumination_delimiter": "Dnot"}},
            80: {"paragraph_fits_on_page": True},
            81: {
                "typo_and_fix": {  # PDF extraction artifact
                    "typo": "PAY AT TENTION",
                    "fix": "PAY ATTENTION",
                }
            },
            82: {"drop_page": True},
            84: {"paragraph_fits_on_page": True},
            87: {"paragraph_fits_on_page": True},
            88: {"drop_page": True},
            89: {"paragraph_fits_on_page": True},
            90: {"type": "illustration"},
            91: {"chapter_info": {"illumination_delimiter": "Wchange"}},
            92: {"paragraph_fits_on_page": True},
            94: {"drop_page": True},
            96: {"paragraph_fits_on_page": True},
            98: {"paragraph_fits_on_page": True},
            99: {"paragraph_fits_on_page": True},
            100: {"drop_page": True},
            # 101: dalmatians
            102: {"paragraph_fits_on_page": True},
            106: {"drop_page": True},
            111: {"paragraph_fits_on_page": True},
            112: {"drop_page": True},
            114: {"paragraph_fits_on_page": True},
            117: {"paragraph_fits_on_page": True},
            118: {"drop_page": True},
            119: {"paragraph_fits_on_page": True},
            123: {"paragraph_fits_on_page": True},
            124: {"type": "illustration"},
            125: {
                "chapter_info": {"illumination_delimiter": "Wawareness"},
                "paragraph_fits_on_page": True,
            },
            128: {"type": "illustration"},
            132: {"paragraph_fits_on_page": True},
            133: {
                "type": "illustration",
                # By default illustrations have no header, unless ... they do
                "header": True,
            },
            134: {"type": "illustration"},
            135: {
                # In order to remove this chapter definition, one needs to
                # deal with patterning distinction between chapter and
                # sub-chapter
                "type": "chapter",
                "chapter_info": {
                    "name": "Continuing the Work",
                    "illumination_delimiter": "A remember",
                },
            },
            136: {"paragraph_fits_on_page": True},
            137: {"paragraph_fits_on_page": True},
            138: {"type": "illustration"},
            143: {"paragraph_fits_on_page": True},
            144: {"type": "illustration"},
            145: {"chapter_info": {"illumination_delimiter": "Sour"}},
            147: {"paragraph_fits_on_page": True},
            148: {"paragraph_fits_on_page": True},
            149: {"paragraph_fits_on_page": True},
            150: {"type": "illustration"},
            152: {"paragraph_fits_on_page": True},
            153: {"paragraph_fits_on_page": True},
            154: {"paragraph_fits_on_page": True},
            156: {"type": "illustration"},
            157: {"paragraph_fits_on_page": True},
            158: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Dedication",
                    "illumination_delimiter": None,
                },
                "paragraph_fits_on_page": True,
            },
            159: {"type": "illustration"},  # This Back cover of the book
        }

    @property
    def pages_info(self) -> dict:
        return self._pages_info

    def convert_to_logical_page_number(self, page_number):
        if page_number == 0:
            return "Cover"
        # Deal with the first pages numbering that uses roman numeration
        if page_number >= 1 and page_number <= self.page_numbering_offset + 1:
            return roman.toRoman(page_number).lower()
        else:
            return str(page_number - self.page_numbering_offset)

    def _page_is_illustration(self, page_number):
        if not page_number in self.pages_info:
            return False
        if not "type" in self.pages_info[page_number]:
            return False
        if self.pages_info[page_number]["type"] == "illustration":
            return True
        return False

    ##### Header related thingies

    def _page_is_headless(self, page_number):
        # Only illustrations can be headless
        if not self._page_is_illustration(page_number):
            return False
        # Yet some illustrations still have a header
        if "header" in self.pages_info[page_number]:
            return False
        # Eventually illustrations not flagged as having a header are headless
        return True

    def _page_is_skipped(self, page_number):
        return self._page_is_illustration(page_number) or self._page_is_dropped(
            page_number
        )

    def book_title_page_header(self, page_number):
        return (
            self.convert_to_logical_page_number(page_number) + r" \| " + self.book_title
        )

    def get_chapter_name(self, extracted_page):
        # Two stages must be distinguished:
        # - Prior to the construction of the chapter of this page: in this case
        #   the chapter name still stands within the extracted_page content
        #   awaiting to be extracted.
        # - Post construction of the chapter of this page: in which case the
        #   content of the extracted_page no longer contains the name the
        #   chapter. This is because the name of the chapter was extracted
        #   (or removed) from the content of the page and passed to the
        #   constructor of the Chapter object for it to be stored). We must
        #   thus retrieve the name of chapter out of the Chapter object itself.
        # The DocumentBreaker constructs the chapter of a page, and records its
        # name on the extracted page, before the text of that page is
        # sanitized: the extracted page is thus the place to retrieve the name
        # from (see ExtractedPage.chapter_name).
        return extracted_page.chapter_name

    def chapter_page_header(self, extracted_page):
        return (
            self.get_chapter_name(extracted_page)
            + r" \| "
            + self.convert_to_logical_page_number(extracted_page.page_number)
        )

    def get_page_header(self, extracted_page):
        page_number = extracted_page.page_number
        if page_number < 0 or page_number > self.total_page_number:
            raise ConverterError(f"Page number {page_number} is outside of book page numeration.")

        # Pages explicitly flagged as headless, well, are headless:
        if self._page_is_headless(page_number):
            return ""

        # First headers of pages starting a new chapter have that new
        # chapter name as header
        if self.get_chapter_splitter().holds_new_chapter(extracted_page):
            return self.get_chapter_name(extracted_page)

        ####### Concerning the Preamble (from page 0 to 20 included)
        # Before the body of the book, there is a (quite lengthy) preamble that
        # has quite specific header rules :
        if page_number < 10:
            # Default value for a preamble header is to be empty
            return ""
        if page_number >= 10 and page_number < 15:
            return roman.toRoman(page_number).lower()
        if page_number == 16:
            # The following hardcoded value for page 16 is because that page
            # doesn't follow the above logical rule. The following fix for page
            # 16 _is_ correct ! It is the pdf that is erroneous.
            return roman.toRoman(16).lower() + roman.toRoman(16).lower()
        if page_number == 17:
            return ""
        if page_number >= 18 and page_number < 20:
            return self.convert_to_logical_page_number(page_number)
        if page_number <= 19 and page_number <= 21:
            return ""

        ####### Concerning the body of the book.
        # Pages of the body of the book, have a headers that follow a simple
        # constructive rule with some exceptions...

        if (page_number % 2) == 0:
            # Odd pages have a header that is simply the book title followed
            # by their page number
            return self.book_title_page_header(page_number)
        if (page_number % 2) != 0:
            if page_number == 133:
                # Page 133 has a brain damaged header that doesn't
                # follow the even page header rule (although it is a near
                # miss). The only possible fix is to define an exception:
                logical_page_number = self.convert_to_logical_page_number(133)
                return (
                    self.book_title
                    + self.get_chapter_name(extracted_page)
                    # The header is used as a regex: the pipes must be escaped
                    # and the exact spacing of the pdf text must be matched.
                    + r"\s*\| \| "
                    + logical_page_number
                    + logical_page_number
                )
            else:
                # Even pages have a different header pattern based on the current
                # chapter name
                return self.chapter_page_header(extracted_page)

        raise ConverterError(f"Header for page number {page_number} is not defined")

    def sanitize_page_text(self, extracted_page):
        self._sanitizer.sanitize_page_text(extracted_page)
