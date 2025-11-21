from reportlab.pdfgen import canvas

def create_pdf(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Hello, TUI PDF Viewer!")
    c.drawString(100, 730, "This is page 1.")
    c.showPage()
    c.drawString(100, 750, "This is page 2.")
    c.drawString(100, 730, "Navigation works!")
    c.save()

if __name__ == "__main__":
    create_pdf("sample.pdf")
