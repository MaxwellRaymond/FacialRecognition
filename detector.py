from pathlib import Path
import face_recognition
import pickle

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

Path("training").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)
Path("validation").mkdir(exist_ok=True)

def encode_known_faces(model: str = "hog", encodings_locations: Path = DEFAULT_ENCODINGS_PATH) -> None:
    names = []
    encodings = []
    image_extensions = {".jpg", ".jpeg", ".png"}

    for filepath in Path("training").glob("*/*"):
        if filepath.suffix.lower() not in image_extensions:
            continue
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)

        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

    name_encodings = {"names": names, "encodings": encodings}
    with encodings_locations.open(mode="wb") as f:
        pickle.dump(name_encodings, f)

encode_known_faces()


        