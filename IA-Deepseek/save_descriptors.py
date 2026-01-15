
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
    descriptors_files_name = ["9ANO_EF_MAT.txt","5ANO_EF_MAT.txt" ,"5ANO_EF_POR.txt", "9ANO_EF_POR.txt", "3ANO_EM_POR.txt", "3ANO_EM_MAT.txt"]
    db = SessionLocal()
    save_descriptors = SaveDescriptors(db)

    for descriptors_file_name in descriptors_files_name:
        print(f"📄 Carregando arquivo de descritores: {descriptors_file_name}")
        with open(Path(f"Material de Referencia/Descritores/{descriptors_file_name}"), "r", encoding="utf-8") as f:
                descriptor_list = f.readlines()
                print(f"📄 {len(descriptor_list)} descritores carregados com sucesso!")

        for descriptor in descriptor_list:
            descriptor_data = {
                "name": descriptor.split("–")[0].strip(),
                "content": descriptor.split("–")[1].strip(),
                "year": descriptors_file_name.split("_")[0].strip(),
                "classroom": descriptors_file_name.split("_")[1].strip(),
                "discipline": descriptors_file_name.split("_")[2].split(".")[0].strip()
            }
            saved_descriptor = save_descriptors.save(descriptor_data)
            print(f"Saved Descriptor ID: {saved_descriptor.id}")