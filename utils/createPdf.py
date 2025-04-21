import os
import tempfile
from pathlib import Path
import streamlit as st
import PyPDF2
from docx import Document
from openai import OpenAI
from fpdf import FPDF
import re

# cover letter text to pdf
def strip_unicode(s):
    replacements = {
        '‘': "'", '’': "'", '“': '"', '”': '"',
        '–': '-', '—': '-', '−': '-', '…': '...',
    }
    for orig, repl in replacements.items():
        s = s.replace(orig, repl)
    s = re.sub(r'[^\x00-\x7F]+', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def text_to_pdf(text, output_filename, n_last_lines=1, line_height=7, font_size=12):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=font_size)
    
    lines = [strip_unicode(line) for line in text.strip().splitlines()]

    n_last_lines = min(n_last_lines, len(lines))
    if n_last_lines < 0:
        n_last_lines = 0

    main_body = lines[:-n_last_lines] if n_last_lines > 0 else lines
    ending_block = lines[-n_last_lines:] if n_last_lines > 0 else []

    cell_width = pdf.w - pdf.l_margin - pdf.r_margin
    if cell_width <= 0:
         raise ValueError("Calculated cell width is zero or negative. Check page size and margins.")

    for line in main_body:
        pdf.set_x(pdf.l_margin)
        if line.strip() == "":
            pdf.ln(line_height)
        else:
            pdf.multi_cell(cell_width, line_height, line)

    # page break for ending the block
    if ending_block:
        needed_height = 0
        current_cell_width = pdf.w - pdf.l_margin - pdf.r_margin
        if current_cell_width <= 0:
             raise ValueError("Calculated cell width is zero or negative before ending block.")

        page_break_trigger_y = pdf.h - pdf.b_margin

        if pdf.get_y() + needed_height > page_break_trigger_y:
            pdf.add_page()
            # cell_width after adding a new page
            cell_width = pdf.w - pdf.l_margin - pdf.r_margin
            if cell_width <= 0:
                raise ValueError("Calculated cell width is zero or negative after add_page.")
        else:
            cell_width = current_cell_width


        # for end block
        for line in ending_block:
            pdf.set_x(pdf.l_margin)
            if line.strip() == "":
                pdf.ln(line_height) 
            else:
                pdf.multi_cell(cell_width, line_height, line)

    pdf.output(output_filename)

# create a pdf
def create_pdf(cover_letter_text, filename_prefix):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        output_path = tmpfile.name
    text_to_pdf(cover_letter_text, output_path)
    return output_path