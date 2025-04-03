from models.gun import Prefix, Postfix, RedText
from sqlalchemy.orm import sessionmaker

import os
import json


def load_prefab_data(engine):
    datapath = "./backend/database_utils/data/"

    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)
    # Create a Session
    session = Session()
    try:
        for clazz in [Prefix, Postfix, RedText]:
            file_path = os.path.join(datapath, f"{clazz.__name__.lower()}.json")

            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue

            with open(file_path, "r") as file:
                data = json.load(file)

            instances = [clazz(**item) for item in data]

            session.add_all(instances)
        session.commit()
    except:
        session.rollback()
    session.close()
