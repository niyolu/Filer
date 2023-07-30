import sys
sys.path.append("..")

from app import crud, database, config, models
from app.models import User, Directory, File, StorageObject

print(config.get_settings())

database.Base.metadata.create_all(bind=database.engine)


session = next(database.get_db())

# Test data
def create_sample_data():
    # Create users
    users = session.query(models.User).all()
    # for user in users:
    #     print(user)
    #     session.delete(user)
    
    session.commit()
    
    session.query(models.User).delete()
    session.query(models.Group).delete()
    session.commit()
    try:
        user1 = User(username="User1", hashed_password="bye")
        user2 = User(username="User2", hashed_password="bye")
        user3 = User(username="User3", hashed_password="bye", root=None)

        # Create directories
        root1 = Directory(name="Root1", path="/", owner=user1)
        root2 = Directory(name="Root2", path="/", owner=user2)
        root3 = Directory(name="Root3", path="/", owner=user2)
        dir1 = Directory(name="Dir1", path="/Dir1", owner=user1)
        dir2 = Directory(name="Dir2", path="/Dir2", owner=user2)
        dir3 = Directory(name="Dir3", path="/Dir3", owner=user3)
        subdir1 = Directory(name="Subdir1", path="/Dir1/Subdir1", owner=user1)
        
        user1.root = root1
        user2.root = root2
        user3.root = root3

        # Create files
        file1 = File(name="File1.txt", path="/Dir1/File1.txt", filetype="text", content=b"Hello, this is File1!", owner=user1)
        file2 = File(name="File2.txt", path="/Dir1/File2.txt", filetype="text", content=b"Hello, this is File2!", owner=user1)
        file3 = File(name="File3.txt", path="/Dir2/File3.txt", filetype="text", content=b"Hello, this is File3!", owner=user2)

        # Build the hierarchy
        root1.children.extend([dir1])
        root2.children.extend([dir2])
        dir1.children.append(subdir1)
        dir1.children.extend([file1, file2])
        dir2.children.append(file3)

        # Add data to the session
        session.add_all([user1, user2, user3])
        session.commit()
    except Exception as e:
        session.rollback()
        print("IGNORING:", e)    
    print_sample_data(session)
    
def print_sample_data(session):
    users = crud.get_users(session)
    for user in users:
        print(user)
        owned_objects = user.owned_objects
        for obj in owned_objects:
            print(obj)
            if isinstance(obj, File):
                print("content")
                print(obj.content.decode())
        

# CRUD Utility Functions
def create_storage_object(name, path, type, owner, parent=None):
    storage_object = StorageObject(name=name, path=path, type=type, owner=owner, parent=parent)
    session.add(storage_object)
    session.commit()
    return storage_object

def create_file(name, path, filetype, content, owner, parent=None):
    file = File(name=name, path=path, filetype=filetype, content=content, owner=owner, parent=parent)
    session.add(file)
    session.commit()
    return file

def create_directory(name, path, owner, parent=None):
    directory = Directory(name=name, path=path, owner=owner, parent=parent)
    session.add(directory)
    session.commit()
    return directory

def get_storage_object_by_id(id):
    return session.query(StorageObject).get(id)

def get_file_by_id(id):
    return session.query(File).get(id)

def get_directory_by_id(id):
    return session.query(Directory).get(id)

def update_storage_object(storage_object, **kwargs):
    for key, value in kwargs.items():
        setattr(storage_object, key, value)
    session.commit()

def delete_storage_object(storage_object):
    session.delete(storage_object)
    session.commit()
    


def main():
    create_sample_data()
    
if __name__ == "__main__":
    main()