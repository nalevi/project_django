from django.db import models, IntegrityError

from .models import Project
from .contants import DATABASE_CREATE_ERROR, OK

def create_project(createMame, createCode, createOwner_id):
    new_proj = Project(name=createMame, code=createCode, project_owner=createOwner_id)
    try:
        new_proj.save()
    except IntegrityError as e:
        print(e.message)
        return DATABASE_CREATE_ERROR

    return OK