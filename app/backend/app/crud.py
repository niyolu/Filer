from sqlalchemy.orm import Session, joinedload

import models, utils, auth


def flatten(list):
    return sum(list, [])


def get_users(db: Session) -> models.User:
    return (
        db.query(models.User)
        .order_by(models.User.id)
        .all()
    )
    

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_id_by_username(db: Session, username: str):
    user = get_user_by_username(db, username)
    return user.id if user else None


def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def get_groups(db: Session):
    return db.query(models.Group).all()


def get_group_by_username(db: Session, groupname: str):
    return db.query(models.Group).filter(models.Group.name == groupname).first()


def get_user_groups(db: Session, user_id: int):
    return get_user(db, user_id).group_memberships


def get_storageobjects(db: Session):
    return (
        db.query(models.StorageObject)
        .order_by(models.StorageObject.id)
        .all()
    )
    

def get_storageobject(db: Session, obj_id: int):
    return db.query(models.StorageObject).filter(models.StorageObject.id == obj_id).first()


def get_storageobject_by_path(db: Session, user_id: int, path: str):
    return db.query(models.StorageObject).filter_by(owner_id=user_id, path=path).first()


def get_storageobject_id_by_path(db: Session, user_id: int, path: str):
    obj = get_storageobject_by_path(db, user_id, path)
    return obj.id if obj else None


def get_shared_group_objs(db: Session, group_id: int):
    return get_group(db, group_id).shared_objects


def get_owned_objs(db: Session, user_id: int):
    return get_user(db, user_id).owned_objects


def get_shared_objs(db: Session, user_id: int):
    return get_user(db, user_id).shared_objects


def create_user(db: Session, username: str, hashed_password: str):
    if get_user_by_username(db, username) is not None:
        return
    user = models.User(username=username, hashed_password=hashed_password)
    root_dir = models.Directory(name="/", path="/", owner=user)
    user.root = root_dir
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_storage_object(
    db: Session,
    user_id: int,
    path: str,
    filename: str,
    content: bytes | None = None
) -> models.StorageObject:
    if "/" not in path:
        raise ValueError("Invalid path.")
    
    parent: models.Directory = get_storageobject_by_path(db, user_id, path)
    if not parent:
        raise ValueError("Invalid parent directory path.")
    assert isinstance(parent, models.Directory), f"{parent} is not a directory but a : {type(parent)}"
    
    if path[-1] == "/":
        path = path[:-1]
    
    owner: models.User = get_user(db, user_id)
    
    obj_path = f"{path}/{filename}"

    if len(parent.children) >= owner.max_objects_per_dir:
        raise PermissionError("Exceeds max objects per directory limit.")
    
    if content:
        new_used = owner.used + len(content)
        if new_used > owner.quota:
            raise PermissionError("Exceeds user's storage quota.")
        owner.used = new_used
        filetype = utils.file_type_from_extension(filename)
        file = models.File(name=filename, owner=owner, content=content, parent=parent, filetype=filetype, path=obj_path)
        db.add(file)
        db.commit()
        db.refresh(file)
        return file
    else:
        directory = models.Directory(name=filename, owner=owner, parent=parent, path=obj_path)
        db.add(directory)
        db.commit()
        db.refresh(directory)
        return directory


def get_permission_for_user_and_object(db: Session, user_id: int, obj_id: int | None = None):
    if obj_id is None:
        return None
    user: models.User = get_user(db, user_id)

    def check_permission(obj):
        if obj in user.owned_objects:
            return "RW"

        if obj in user.shared_objects:
            share = (
                db.query(models.StorageShare)
                .filter_by(user_id=user_id, obj_id=obj.id)
                .first()
            )
            return share.permission if share else None

        for group in user.group_memberships:
            if obj in group.shared_objects:
                share = (
                    db.query(models.GroupShare)
                    .filter_by(group_id=group.id, obj_id=obj.id)
                    .first()
                )
                return share.permission if share else None

        return None

    obj = db.query(models.StorageObject).options(joinedload(models.StorageObject.parent)).filter_by(id=obj_id).first()
    while obj is not None:
        permission = check_permission(obj)
        if permission is not None:
            return permission
        obj = obj.parent

    return None


def change_active_status_for_user_by_username(db: Session, username: str, state: bool):
    user: models.User = get_user_by_username(db, username)
    user.is_active = state
    db.commit()
    db.refresh(user)
    return user


def share_storage_object_with_user(db: Session, obj_id: int, from_user_id: int, to_user_id: int, permission: str):
    obj = get_storageobject(db, obj_id)
    
    if obj.owner_id != from_user_id:
        raise PermissionError("You can only share objects owned by you.")

    if not db.query(models.StorageShare).filter_by(user_id=to_user_id, obj_id=obj_id).first():
        share = models.StorageShare(user_id=to_user_id, obj_id=obj_id, permission=permission)
        db.add(share)
        db.commit()
        db.refresh(share)
        return share


def share_storage_object_with_group(db: Session, obj_id: int, group_id, permission: str):
    obj = get_storageobject(db, obj_id)
    owner = obj.owner
    group = get_group(db, group_id)
    if not owner in group.members:
        raise PermissionError("You can only share with groups you are part of.")
    
    if not db.query(models.GroupShare).filter_by(group_id=group_id, obj_id=obj_id).first():
        share = models.GroupShare(group_id=group_id, obj_id=obj_id, permission=permission)
        db.add(share)
        db.commit()
        db.refresh(share)
        return share
    

def delete_object_by_path(db: Session, user_id: int, path: str):
    object = get_storageobject_by_path(db, user_id, path)
    if not object:
        raise ValueError("Invalid path.")
    if isinstance(object, models.File):
        owner = object.owner
        owner.used -= len(object.content)
    db.delete(object)
    db.commit()
    return object


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    return user


def get_all_objs(db: Session, user_id):
    user = get_user(db, user_id)
    owned_objs = user.owned_objects
    shared_objs = user.shared_objects
    group_shared_objs = {group.name: group.shared_objects for group in user.group_memberships}
    return owned_objs, shared_objs, group_shared_objs
    
    
def add_user_to_group(db: Session, group_id: int, user_id: int):
    group: models.Group = get_group(db, group_id)
    user: models.User = get_user(db, user_id)
    group.members.append(user)
    db.commit()
    return group
    
    
def change_user_quota(db: Session, user_id: int, new_quota: int):
    user = get_user(db, user_id)
    if user.used > new_quota:
        raise ValueError("new_quota cant be smaller than users quote")
    user.quota = new_quota
    db.commit()
    return user


def init_admin(db: Session):
    create_user(db, "root", auth.get_password_hash(auth.settings.app_admin_pw))