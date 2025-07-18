
from pathlib import Path
from models.descriptor import Descriptor
from db import SessionLocal

class SaveDescriptors:
    def __init__(self, db_session):
        self.db_session = db_session

    def save(self, descriptor_data):
        descriptor = Descriptor(**descriptor_data)
        self.db_session.add(descriptor)
        self.db_session.commit()
        return descriptor
    
if __name__ == "__main__":
    descriptors_file_name = "3ANO_EM_MAT.txt"
    db = SessionLocal()
    save_descriptors = SaveDescriptors(db)

    print(f"📄 Carregando arquivo de descritores: {descriptors_file_name}")
    with open(Path(f"Material de Referencia/Descritores/{descriptors_file_name}"), "r", encoding="utf-8") as f:
                descriptor_list = f.readlines()
                print(f"📄 {len(descriptor_list)} descritores carregados com sucesso!")

    for descriptor in descriptor_list:
        descriptor_data = {
            "name": descriptor.split("–")[0],
            "content": descriptor.split("–")[1],
            "year": descriptors_file_name.split("_")[0],
            "classroom": descriptors_file_name.split("_")[1],
            "discipline": descriptors_file_name.split("_")[2].split(".")[0]
        }
        saved_descriptor = save_descriptors.save(descriptor_data)
    print(f"Saved Descriptor ID: {saved_descriptor.id}")