
# import crud, models, database

# models.Base.metadata.create_all(bind=database.engine)

# db = next(database.get_db())

# for user in crud.get_users(db):
#     db.delete(user)
    
# for group in crud.get_groups(db):
#     db.delete(group)
    
# db.commit()


# def create_test_user(db, username="testuser", hashed_password="testpassword"):
#     return crud.create_user(db, username=username, hashed_password=hashed_password)


# def test_create_storage_hierarchy(db_session):
#     user = create_test_user(db_session)
#     dir1 = crud.create_storage_object(db_session, user.id, "/", "dir1")
#     dir2 = crud.create_storage_object(db_session, user.id, "/dir1", "dir2")
#     dir3 = crud.create_storage_object(db_session, user.id, "/dir/dir2", "dir3")
#     file1 = crud.create_storage_object(db_session, user.id, "/dir/dir2", "file1")
#     file2 = crud.create_storage_object(db_session, user.id, dir2.path, "file1")
#     print(dir1)
#     assert False
#     assert owned_obj.content == b"Content"
#     assert owned_obj.path == "/file.txt"
    
# test_create_storage_hierarchy(db)


import pydantic

class A(pydantic.BaseModel):
    i: int
    j: int

class _A:
    def __init__(self, j=None):
        self.i = 1
        self.j = j

print(_A().__dict__)  
print(A(i=1))
print(A.model_validate(_A(), context=dict(j=3)))