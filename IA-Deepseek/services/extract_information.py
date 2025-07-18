from pathlib import Path
import pdfplumber

class ExtractInfo:
    def __init__(self, pdf_path = Path("")):
        self.pdf_path = pdf_path

    def extract_text(self):
        """Extrai informações em texto de um arquivo PDF"""
        print(f"Extraindo texto do PDF: {self.pdf_path}")
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            print(f"{len(pdf.pages)} página(s) encontrada(s).")
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        print(f"Texto extraído do PDF: {self.pdf_path}")
        return text

    def save_results(self, pdf_text="", txt_output_path=None):
        """Salva o texto extraído em um arquivo .txt"""
        path = Path("Material de Referencia/Informações Extraidas dos PDFs")
        if txt_output_path is None:
            txt_output_path = self.pdf_path.stem + ".txt"
        print(f"Salvando texto extraído em: {path / txt_output_path}")
        with open(path / txt_output_path, 'w', encoding='utf-8') as f:
            f.write(pdf_text)
        print(f"Texto do PDF salvo em: {path / txt_output_path}")

