import sys
import re


class Sanitizer:
    """Sanitizer for Collecting Gold Dust book."""

    def __init__(self, structural_info, get_page_header):
        self.structural_info = structural_info
        self.chapter_splitter = structural_info.get_chapter_splitter()
        self.get_page_header = get_page_header

    def sanitize_page_text(self, extracted_page):
        """
        After extraction of the text from the original pdf, some ad hoc
        manual cleaning is alas required e.g. remove the header of the page.
        """
        self._sanitize_remove_header(extracted_page)
        if self.chapter_splitter.holds_new_chapter(extracted_page):
            self._sanitize_fix_illumination(extracted_page)

    def _sanitize_remove_header(self, extracted_page):
        if self.chapter_splitter.holds_new_chapter(extracted_page):
            # Chapters have no headers
            return

        header_less_page_text = extracted_page.text
        # Make sure the exact header text is encountered
        header_text = self.get_page_header(extracted_page)
        if not re.match("^" + header_text, header_less_page_text):
            print(
                "Header <<",
                header_text,
                ">> not found on pdf page ",
                extracted_page.page_number,
                " ",
                end="",
            )
            print(
                "(that is reader page number ",
                extracted_page.page_layout.reader_page_number,
                ")",
            )
            original_page_text = extracted_page.original_pdf_page.extract_text(
                extraction_mode="layout"
            )
            print("Pdf original text : ", repr(original_page_text))
            print("Exiting.")
            sys.exit()
        # Proceed with the removal of the header
        # Only remove the header found at the very beginning of the page:
        # an unanchored removal would also strip e.g. every "x" of the body
        # when the header is the page number "x".
        header_less_page_text = re.sub(
            "^" + header_text, "", header_less_page_text, count=1
        )
        # Eventually, remove some possibly leaving whitespaces
        header_less_page_text = header_less_page_text.lstrip()
        # Eventually update the extracted_page
        extracted_page.text = header_less_page_text

    def _sanitize_fix_illumination(self, extracted_page):
        """Chapters beginnings (that is the first page of a new chapter) start
        with an illumination (decorated first letter) that confuses pypdf.
        The letter of the illumination ends mixed up within the text of the
        first sentence of the chapter. Fix that.
        """
        page_number = extracted_page.page_number
        text_to_fix = extracted_page.text
        if not self.chapter_splitter.holds_new_chapter(extracted_page):
            print("Erroneous call to Sanitizer::_sanitize_fix_illumination()")
            print("  This extracted page does not seem to be a chapter starting page.")
            print("  Extracted page: ", extracted_page)
            print("  Exiting")
            sys.exit()

        delimiter = self.structural_info._get_chapter_info(page_number)[
            "illumination_delimiter"
        ]
        if delimiter is None:
            # This chapter has no illumination to fix (probably because there
            # is no illumination at all). Return the original text:
            return

        # The illumination character that got embedded in the text happens to
        # to always be preceded by a return character. Looking for the delimiter
        # prefixed with a return character will make the result a little more
        # secure (yet not foolproof):
        delimiter_with_return = "[\n]" + delimiter
        match = re.search(delimiter_with_return, text_to_fix)
        if not match:
            print(
                "Delimiter ",
                repr(delimiter),
                "not found within illumination for extracted page:",
            )
            print(extracted_page)
            print("Exiting.")
            sys.exit()
        if len(match.groups()) > 1:
            print(
                "Multiple occurrences of delimiter ",
                repr(delimiter),
                "within illumination for extracted page:",
            )
            print(extracted_page)
            print("Exiting.")
            sys.exit()

        # We shall only "fix" on the illumination concerned part of the text,
        # that is the text appearing before the delimiter. We thus split the
        # text in two parts:
        # - illumination_part: the part of the text that is prior to the
        #   delimiter and on which we shall proceed with modifications
        # - end_of_text: the remaining of the text that shall remain unchanged.
        illumination_part = text_to_fix[: match.end()]
        end_of_text = text_to_fix[match.end() :]

        # The first thing to do is to remove the illumination character from
        # the text. We use this opportunity to replace the return character,
        # that prefixed the delimiter, with a whitespace:
        corrected_snippet = delimiter[1:]
        illumination_part = re.sub(
            delimiter_with_return, " " + corrected_snippet, illumination_part
        )
        # The second thing to do is to reinsert the illumination character
        # within the text. It belongs right before the first word of the
        # paragraph, that is the first indented line. Note that this is not
        # always the very beginning of the text: some chapters have a title
        # line (e.g. "CAUSE AND EFFECT CHAIN") standing prior to the paragraph.
        paragraph_start = re.search(r"^ +(?=\S)", illumination_part, re.MULTILINE)
        if paragraph_start:
            # The hand made indentation is dropped (it would be overwritten
            # by the illumination drawing of the leading character)
            title_part = illumination_part[: paragraph_start.start()]
            paragraph_part = illumination_part[paragraph_start.end() :]
        else:
            title_part = ""
            paragraph_part = illumination_part
        # Eventually remove the occurrence (or the couple occurrences) of
        # returns + whitespaces that were added to reserve some space for the
        # illuminations on the second or third line of the text. Only the
        # paragraph is concerned (the title, if any, must keep its own line).
        # The following does work but goes too far...
        paragraph_part = re.sub("(\n( *))", " ", paragraph_part)
        # When the illumination character is a word on its own (e.g. "A
        # remember") it must be separated from the first word of the paragraph
        illumination_character = delimiter[0]
        if corrected_snippet[:1].isspace():
            illumination_character += " "
        illumination_part = title_part + illumination_character + paragraph_part
        # The third fix consists in removing the hand made spacing of the
        # beginning of the text (that would be overwritten by the illumination
        # drawing of the leading character):
        illumination_part = re.sub(
            self.chapter_splitter.separator_regex + "( *)",
            "",
            illumination_part,
        )

        # Eventually update the extracted_page
        extracted_page.text = illumination_part + end_of_text
