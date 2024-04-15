import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import argparse

def new_page(content, width=1920, height=1080):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    can.setFont("Times-Roman", 10)
    can.drawString(0.1*width, 0.9*height, content)
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    return packet

def pdf_editor(source, target, content):
    pdf_file = open(source, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    pdf_writer = PyPDF2.PdfWriter()

    for page_num in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    page = pdf_reader.pages[len(pdf_reader.pages) - 1]
    new_pdf = new_page(content, width=page.mediabox.width, height=page.mediabox.height)
    new_content_page = PyPDF2.PdfReader(new_pdf).pages[0]
    page.merge_page(new_content_page)

    pdf_writer.add_page(new_content_page)

    pdf_output_file = open(target, 'wb')
    pdf_writer.write(pdf_output_file)

    pdf_output_file.close()
    pdf_file.close()

def main():
    parser = argparse.ArgumentParser(description="PDF editor")
    parser.add_argument("--input", help="input PDF file")
    parser.add_argument("--output", help="output PDF file")
    parser.add_argument("--content", help="Content to add to the PDF file")
    args = parser.parse_args()

    pdf_editor(args.input, args.output, args.content)



if __name__ == "__main__":
    main()