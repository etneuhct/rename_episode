import os.path
from enum import Enum
from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel

from rename import Rename

app = FastAPI()


class RenameMethod(str, Enum):
    regex = "regex"
    order = "order"


class RenameRequest(BaseModel):
    folder: str
    method: RenameMethod
    season: Optional[int] = None
    season_regex: Optional[str] = None
    episode_regex: Optional[str] = r"[Ss](\d+)[Ee](\d+)"
    dry: bool = True


@app.post("/rename")
def rename(request: RenameRequest = Body(...)):
    folder_path = os.path.join("./data", request.folder)
    renamer = Rename(folder_path)

    if request.method == RenameMethod.regex:
        percentage, info = renamer.renommer_avec_regex(
            season=request.season,
            season_regex=request.season_regex,
            episode_regex=request.episode_regex,
            dry=request.dry
        )
        return {
            "percentage": percentage,
            "info": info
        }
    else:
        return {
            "error": "Méthode 'order' non encore implémentée"
        }
