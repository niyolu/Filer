from sqlalchemy.orm import Session

import crud, database, config, models
#from app.models import User, Directory, File, StorageObject

import pytest

print(config.get_settings())

models.Base.metadata.create_all(bind=database.engine)


@pytest.fixture
def db_session():
    session = next(database.get_db())
    session = database.local_session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


# Helper function to create a new user for testing
def create_test_user(db, username="testuser", hashed_password="testpassword"):
    return crud.create_user(db, username=username, hashed_password=hashed_password)

# Helper function to create a new group for testing
def create_test_group(db, groupname="testgroup"):
    group = models.Group(name=groupname)
    db.add(group)
    db.commit()
    return group


@pytest.fixture(autouse=True)
def setup_test_data(db_session):
    # Clean up any existing data and ensure a fresh state for each test
    # db_session.query(models.StorageObject).delete()
    
    for user in crud.get_users(db_session):
        db_session.delete(user)
        
    for group in crud.get_groups(db_session):
        db_session.delete(group)
        
    db_session.commit()
    
    
comp_obj_non_nested = lambda x,y: x.name == y.name and x.path == y.path and x.id==y.id and x.owner==y.owner and x.content == y.content if isinstance(x, models.File) else True
    

# Unit tests
def test_create_user(db_session):
    user = create_test_user(db_session)
    assert user.id is not None
    assert user.username == "testuser"

def test_get_user_by_username(db_session):
    user= create_test_user(db_session)
    found_user = crud.get_user_by_username(db_session, "testuser")
    assert found_user is not None
    assert found_user.id == user.id

def test_create_group(db_session):
    group = create_test_group(db_session)
    assert group.id is not None
    assert group.name == "testgroup"
    
def test_add_user_to_group(db_session):
    user = create_test_user(db_session)
    group = create_test_group(db_session)
    crud.add_user_to_group(db_session, group_id=group.id, user_id=user.id)
    
    user_groups = crud.get_user_groups(db_session, user_id=user.id)
    assert group in user_groups

def test_change_active_status_for_user_by_username(db_session):
    user = create_test_user(db_session)
    assert user.is_active is True
    
    updated_user = crud.change_active_status_for_user_by_username(db_session, "testuser", False)
    assert updated_user.is_active is False
 
def test_create_storage_object(db_session):
    user = create_test_user(db_session)
    owned_obj = crud.create_storage_object(db_session, user.id, "/", "file.txt", content=b"Content")
    assert owned_obj.content == b"Content"
    assert owned_obj.path == "/file.txt"

def test_create_storage_hierarchy(db_session):
    user = create_test_user(db_session)
    dir1 = crud.create_storage_object(db_session, user.id, "/", "dir1")
    dir2 = crud.create_storage_object(db_session, user.id, "/dir1", "dir2")
    dir3 = crud.create_storage_object(db_session, user.id, "/dir1/dir2", "dir3")
    file1 = crud.create_storage_object(db_session, user.id, "/dir1/dir2", "file1", content=b"1")
    file2 = crud.create_storage_object(db_session, user.id, dir3.path, "file2", content=b"2")
    
    assert file1.path == "/dir1/dir2/file1"
    assert file2.path == "/dir1/dir2/dir3/file2"
    
def test_share_storage_object_with_user(db_session):
    user1 = create_test_user(db_session, "user1")
    user2 = create_test_user(db_session, "user2")
    shared_obj = crud.create_storage_object(db_session, user1.id, "/", "shared.txt", content=b"Shared content")
    assert shared_obj in user1.owned_objects
    share = crud.share_storage_object_with_user(db_session, shared_obj.id, user1.id, user2.id, "R")
    assert share is not None
    assert len(user2.shared_objects) == 1
    assert user2.shared_objects[0] == shared_obj

def test_group_share_storage_object(db_session):
    user1 = create_test_user(db_session, "user1")
    user2 = create_test_user(db_session, "user2")
    group = create_test_group(db_session)
    group.members.extend([user1, user2])
    group_shared_obj = crud.create_storage_object(db_session, user2.id, "/", "group_shared.txt", content=b"Group shared content")
    share = crud.share_storage_object_with_group(db_session, group_shared_obj.id, group.id, "R")
    assert share is not None
    assert group_shared_obj in user1.group_memberships[0].shared_objects

def test_get_all_objs(db_session):
    user = create_test_user(db_session)
    other_user = create_test_user(db_session, username="testuser2")
    owned_obj = crud.create_storage_object(db_session, user.id, "/", "owned.txt", content=b"Owned content")
    shared_obj = crud.create_storage_object(db_session, other_user.id, "/", "shared.txt", content=b"Shared content")
    group_shared_obj = crud.create_storage_object(db_session, other_user.id, "/", "group_shared.txt", content=b"Group shared content")
    group = create_test_group(db_session)
    group.members.extend([user, other_user])
    share = crud.share_storage_object_with_user(db_session, shared_obj.id, other_user.id, user.id, "R")
    group_share = crud.share_storage_object_with_group(db_session, group_shared_obj.id, group.id, "R")
    owned_objs, shared_objs, group_shared_objs = crud.get_all_objs(db_session, user.id)

    assert share
    assert group_share
    assert owned_obj in owned_objs
    assert shared_obj in shared_objs
    assert group_shared_obj in group_shared_objs[group.name]
    
def test_change_user_quota(db_session):
    user = create_test_user(db_session)
    new_quota = 1  # 1 MB
    updated_user = crud.change_user_quota(db_session, user.id, new_quota)
    assert updated_user.quota == new_quota
    
def test_delete_object_by_path(db_session):
    user = create_test_user(db_session)
    file_obj = crud.create_storage_object(db_session, user.id, "/", "file.txt", content=b"File content")
    deleted_obj = crud.delete_object_by_path(db_session, user.id, "/file.txt")
    assert deleted_obj[0].id == file_obj.id
    
def test_rename(db_session):
    user = create_test_user(db_session)
    dir1 = crud.create_storage_object(db_session, user.id, "/", "dir1")
    file1 = crud.create_storage_object(db_session, user.id, "/dir1", "file1.txt", content=b"File content1")
    dir2 = crud.create_storage_object(db_session, user.id, "/dir1", "dir2")
    file2 = crud.create_storage_object(db_session, user.id, "/dir1/dir2", "file2.txt", content=b"File content2")
    crud.rename_storageobject(db_session, dir1.id, "dir1changed")
    assert file1.path == "/dir1changed/file1.txt"
    assert file2.path == "/dir1changed/dir2/file2.txt"
    

def test_delete_subobject_by_path(db_session):
    user = create_test_user(db_session)
    file1 = crud.create_storage_object(db_session, user.id, "/", "file1.txt", content=b"File content1")
    dir1 = crud.create_storage_object(db_session, user.id, "/", "dir1")
    file2 = crud.create_storage_object(db_session, user.id, "/dir1", "file2.txt", content=b"File content2")
    dir2 = crud.create_storage_object(db_session, user.id, "/dir1", "dir2")
    file3 = crud.create_storage_object(db_session, user.id, "/dir1/dir2", "file3.txt", content=b"File content3")    
    deleted_objs = crud.delete_object_by_path(db_session, user.id, "/dir1")
    
    assert_objs_deleted = [file2, dir2, file3]

    for obj_to_delete in assert_objs_deleted:
        assert crud.get_storageobject(db_session, obj_to_delete.id) is None, obj_to_delete
        found = False
        for del_obj in deleted_objs:
            if comp_obj_non_nested(obj_to_delete, del_obj):
                found = True
        assert found, obj_to_delete
                
    assert crud.get_storageobject(db_session, file1.id) == file1
    
def test_delete_shared_obj(db_session):
    sharee = create_test_user(db_session, "sharee")
    receivee = create_test_user(db_session, "receivee")
    dir = crud.create_storage_object(db_session, sharee.id, sharee.root.path, "dir")
    file = crud.create_storage_object(db_session, sharee.id, dir.path, "file.txt", content=b"File content")
    share = crud.share_storage_object_with_user(db_session, dir.id, sharee.id, receivee.id, "R")
    assert file in crud.get_subelements(receivee.shared_objects)
    assert dir in receivee.shared_objects
    assert crud.get_permission_for_user_and_object(db_session, receivee.id, file.id) == "R"

def test_delete_user(db_session):
    user = create_test_user(db_session)
    deleted_user = crud.delete_user(db_session, user.id)
    assert deleted_user.id == user.id
    
def test_get_all_objs_tree(db_session):
    sharee = create_test_user(db_session, "sharee")
    initial_objs = crud.get_all_objs_tree(db_session, sharee.id)
    assert not initial_objs.shared_objects
    assert not initial_objs.group_shared_objects
    assert initial_objs.owned_objects.name == "/"
    
    receivee = create_test_user(db_session, "receivee")
    groupsharee1 = create_test_user(db_session, "groupsharee1")
    groupsharee2 = create_test_user(db_session, "groupsharee2")
    
    group = create_test_group(db_session)
    group.members.extend([receivee, groupsharee1, groupsharee2])
    
    owned_file1 = crud.create_storage_object(db_session, receivee.id, receivee.root.path, "file1.txt", content=b"File content1")
    owned_dir1 = crud.create_storage_object(db_session, receivee.id, receivee.root.path, "dir1")
    owned_file2 = crud.create_storage_object(db_session, receivee.id, owned_dir1.path, "file2.txt", content=b"File content2")
    owned_dir2 = crud.create_storage_object(db_session, receivee.id, owned_dir1.path,  "dir2")
    owned_file3 = crud.create_storage_object(db_session, receivee.id, owned_dir2.path, "file3.txt", content=b"File content3")
    
    
    shared_dir = crud.create_storage_object(db_session, sharee.id, sharee.root.path, "dir")
    shared_file = crud.create_storage_object(db_session, sharee.id, shared_dir.path, "file.txt", content=b"File content")
    
    group_shared_obj = crud.create_storage_object(db_session, groupsharee1.id, groupsharee1.root.path, "group_shared.txt", content=b"Group shared content")
    group_shared_obj_remove = crud.create_storage_object(db_session, groupsharee2.id, sharee.root.path, "removefile.txt", content=b"To be removed")

    share = crud.share_storage_object_with_user(db_session, shared_dir.id, sharee.id, receivee.id, "R")
    group_share = crud.share_storage_object_with_group(db_session, group_shared_obj.id, group.id, "RW")
    group_share_remove = crud.share_storage_object_with_group(db_session, group_shared_obj_remove.id, group.id, "R")
    
    midway_objs = crud.get_all_objs_tree(db_session, sharee.id)
    midway_owned = midway_objs.owned_objects
    midway_shared = midway_objs.shared_objects
    midway_group_shared = midway_objs.group_shared_objects
    print(midway_objs)
    print("--\n")
    print(midway_owned.children)
    print(type(midway_owned.children))
    assert any([comp_obj_non_nested(owned_file1, c) for c in midway_owned.children]), midway_owned.children
    assert any([comp_obj_non_nested(owned_dir1, c) for c in midway_owned])
    assert any([comp_obj_non_nested(owned_file2, cc) for c in midway_owned for cc in c.children if isinstance(c, models.Directory)])
    assert any([comp_obj_non_nested(owned_dir2, cc) for c in midway_owned for cc in c.children if isinstance(c, models.Directory)])
    assert any([comp_obj_non_nested(owned_file3, ccc) for c in midway_owned for ccc in cc.children for cc in c.children if isinstance(c, models.Directory) if isinstance(cc, models.Directory)])
    
    
    
if __name__ == "__main__":
    assert False
    test_create_storage_hierarchy(next(db_session()))