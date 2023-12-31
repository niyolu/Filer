from sqlalchemy.orm import Session, joinedload

import collections
import itertools

import models, utils, auth, schemas
from logger import logger


class DuplicateError(Exception):
    pass


def flatten(list):
    return sum(list, [])

def get_users(db: Session) -> models.User:
    return (
        db.query(models.User)
        .order_by(models.User.id)
        .all()
    )
    

def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_id_by_username(db: Session, username: str) -> int | None:
    user = get_user_by_username(db, username)
    return user.id if user else None


def get_group(db: Session, group_id: int) -> models.Group:
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def get_groups(db: Session):
    return db.query(models.Group).all()


def get_group_by_groupname(db: Session, groupname: str) -> models.Group:
    return db.query(models.Group).filter(models.Group.name == groupname).first()


def get_group_by_username(db: Session, username: str) -> models.Group:
    return get_user_by_username(db, username).group_memberships


def get_user_groups(db: Session, user_id: int):
    return get_user(db, user_id).group_memberships


def get_storageobjects(db: Session):
    return (
        db.query(models.StorageObject)
        .order_by(models.StorageObject.id)
        .all()
    )
    

def get_storageobject(db: Session, obj_id: int) -> models.StorageObject:
    return db.query(models.StorageObject).filter(models.StorageObject.id == obj_id).first()


def get_storageobject_by_path(db: Session, user_id: int, path: str) -> models.StorageObject:
    return db.query(models.StorageObject).filter_by(owner_id=user_id, path=path).first()


def get_storageobject_id_by_path(db: Session, user_id: int, path: str) -> int | None:
    obj = get_storageobject_by_path(db, user_id, path)
    return obj.id if obj else None


def get_shared_group_objs(db: Session, group_id: int):
    return get_group(db, group_id).shared_objects


def get_owned_objs(db: Session, user_id: int):
    return get_user(db, user_id).owned_objects


def get_shared_objs(db: Session, user_id: int):
    return get_user(db, user_id).shared_objects


def rename_storageobject(db: Session, obj_id: int, new_name: str) -> models.StorageObject:
    def _update_path(obj: models.StorageObject):
        parent_path = obj.parent.path
        obj.path = f"{parent_path if parent_path != '/' else ''}/{obj.name}"
        if isinstance(obj, models.Directory):
            for child in obj.children:
                _update_path(child)
        
    obj = get_storageobject(db, obj_id)
    obj.name = new_name
    _update_path(obj)


def create_user(
    db: Session,
    username: str,
    hashed_password: str,
    quota: int | None = None,
    max_objects_per_dir: int | None = None
) -> models.User:
    if get_user_by_username(db, username) is not None:
        raise DuplicateError(f"User {username} already exists")
    
    user = models.User(
        username=username, hashed_password=hashed_password,
        quota=quota, max_objects_per_dir=max_objects_per_dir
    )
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
    object_name: str,
    content: bytes | None = None
) -> models.StorageObject:
    if "/" not in path:
        raise ValueError(f"Invalid path ({path}).")
    if "/" in object_name:
        raise ValueError(f"invalid name ({object_name})")
    
    parent: models.Directory = get_storageobject_by_path(db, user_id, path)
    if not parent:
        raise ValueError("Invalid parent directory path.")
    assert isinstance(parent, models.Directory), f"{parent} is not a directory but a : {type(parent)}"
    
    if path[-1] == "/":
        path = path[:-1]
    
    owner = get_user(db, user_id)
    
    obj_path = f"{path}/{object_name}"
    
    old_in_db = get_storageobject_by_path(db, user_id, obj_path)
    
    if old_in_db:
        raise DuplicateError(f"Object {schemas.OwnedFile.model_validate(old_in_db)} already exists")
    
    # logger.debug(f"{old_in_db} doesnt exist yet")

    if len(parent.children) >= owner.max_objects_per_dir:
        raise PermissionError(f"Exceeds max objects per directory limit ({parent.children}/{owner.max_objects_per_dir}).")
    
    if content:
        new_used = owner.used + len(content)
        if new_used > owner.quota:
            raise PermissionError(f"Exceeds user's storage quota ({new_used}/{owner.quota}).")
        owner.used = new_used
        filetype = utils.file_type_from_extension(object_name)
        file = models.File(name=object_name, owner=owner, content=content, parent=parent, filetype=filetype, path=obj_path)
        db.add(file)
        db.commit()
        db.refresh(file)
        return file
    else:
        directory = models.Directory(name=object_name, owner=owner, parent=parent, path=obj_path)
        db.add(directory)
        db.commit()
        db.refresh(directory)
        return directory
    
    
def create_group(db: Session, name: str) -> models.Group:
    if get_group_by_groupname(db, name):
        return DuplicateError(f"Group already exists´({name})")
    group = models.Group(name=name)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def get_permission_for_user_and_object(
    db: Session,
    user_id: int,
    obj_id: int
) -> str | None:

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

    obj = (
        db.query(models.StorageObject)
        .options(joinedload(models.StorageObject.parent))
        .filter_by(id=obj_id)
        .first()
    )
    while obj is not None:
        permission = check_permission(obj)
        if permission is not None:
            return permission
        obj = obj.parent

    return None


def change_active_status_for_user_by_username(db: Session, username: str, state: bool):
    user = get_user_by_username(db, username)
    user.is_active = state
    db.commit()
    db.refresh(user)
    return user


def share_storage_object_with_user(
    db: Session,
    obj_id: int,
    from_user_id: int,
    to_user_id: int,
    permission: str
):
    """Share an existing storage object with another user

    Args:
        db (Session): db session
        obj_id (int): id of object to be shared
        from_user_id (int): owner of object
        to_user_id (int): user to be shared with
        permission (Permission):  Read or Read/Write permission

    Raises:
        PermissionError: insufficient permission to share the object

    Returns:
        StorageShare: ORM share representation
        
    Details:
        if obj is directory dont share subobjects since we look it up to avoid having to update a lot
        
        if obj is shared already inside another directory, dont merge the shared reference so we can seperately
        delete and display them to the client
        
        assume users exist
    """
    
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
    if any (obj.path == g_obj.path for g_obj in group.shared_objects):
        raise DuplicateError(f"File with path={obj.path} already shared with {group.name}")
    
    if not db.query(models.GroupShare).filter_by(group_id=group_id, obj_id=obj_id).first():
        share = models.GroupShare(group_id=group_id, obj_id=obj_id, permission=permission)
        db.add(share)
        db.commit()
        db.refresh(share)
        return share
    

def delete_object(
        db: Session,
        obj: models.StorageObject,
        deleted: list[models.StorageObject] | None = None
    ):
    if not deleted:
        deleted = []
    if isinstance(obj, models.File):
        owner = obj.owner
        owner.used -= len(obj.content)
    else:
        for child in obj.children:
            deleted.extend(delete_object(db, child))
    db.delete(obj)
    db.commit()
    deleted.append(obj)
    return deleted


def delete_object_by_path(db: Session, user_id: int, path: str):
    obj= get_storageobject_by_path(db, user_id, path)
    if not obj:
        raise ValueError(f"Invalid path ({path}).")
    return delete_object(db, obj)


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    return user


# TODO: test
def get_subelements(elements: list[models.StorageObject]):
    working_set = collections.deque(elements if isinstance(elements, list) else [elements])
    subelements = []
    while working_set:
        element = working_set.popleft()
        subelements.append(element)
        match(element):
            case models.Directory(children=children):
                print("type1", models.Directory)
                working_set.extend(children)
            case _:
                print("type2", type(element))
    return subelements


def get_subelements_schema(elements: list[schemas.SharedStorageObject]):
    working_set = collections.deque(elements)
    subelements = []
    while working_set:
        element = working_set.popleft()
        subelements.append(element)
        match(element):
            case schemas.OwnedDirectory(children=children) | schemas.SharedDirectory(children=children):
                print("type1", type(element), "element", element)
                working_set.extend(children)
            case _:
                print("type2", type(element), "element", element)
    return subelements


def get_all_objs(db: Session, user_id: int):
    owned, shared, group_shared = get_all_objs_flat(db, user_id)
    return owned, get_subelements(shared), {g:get_subelements(sh) for g, sh in group_shared.items()}


def get_all_objs_flat(db: Session, user_id: int):
    user = get_user(db, user_id)
    owned_objs = user.owned_objects
    shared_objs = user.shared_objects
    group_shared_objs = {group.name: group.shared_objects for group in user.group_memberships}
    return owned_objs, shared_objs, group_shared_objs
    
    
def get_all_objs_tree(db: Session, user_id: int):
    user = get_user(db, user_id)
    groups: list[models.Group] = user.group_memberships
    share_objects: list[models.StorageObject] = user.shared_objects
    
    def _build(obj):
        return build_tree(db, user.id, obj)
    
    
    # logger.debug(f"{user.root}")
    owned_tree = schemas.OwnedDirectory.model_validate(user.root)
    
    user_shared_objects = collections.defaultdict(list)
    for shared_object in share_objects:
        user_shared_objects[shared_object.owner.username].append(_build(shared_object))

    group_shared_trees = {
        group.name: [_build(obj) for obj in group.shared_objects]
        for group in groups
    }
    # print(f"{type(user_shared_objects)=}")
    # if user_shared_objects.values():
        # print(f"{type(user_shared_objects.values())=}")
        # print(f"{user_shared_objects.values()=}")
    # [print(type(y)) for y in [x for x in user_shared_objects.values()]]
    # [print(type(y)) for y in [x for x in group_shared_trees.values()]]#
    # assert all(isinstance(y, (schemas.SharedDirectory, schemas.SharedFile)) ])
    #assert all(isinstance(y, (schemas.SharedDirectory, schemas.SharedFile)) for y in [x for x in group_shared_trees.values()])
    for k,v in group_shared_trees.items():
        for o in v:
            assert isinstance(o, (schemas.SharedDirectory, schemas.SharedFile)), o
    
    
    # assert isinstance(user_shared_objects, dict[str, schemas.SharedFile | schemas.SharedDirectory])
    # assert isinstance(group_shared_trees, dict[str, list[schemas.SharedFile | schemas.SharedDirectory]])
    
    # logger.debug(f"{type(owned_tree)=}")
    # logger.debug(f"{owned_tree=}")
    file_overview = schemas.StorageOverview(
        owned_objects=owned_tree,
        shared_objects=user_shared_objects,
        group_shared_objects = group_shared_trees
    )
    
    # logger.debug(f"{type(user_shared_objects)=}")
    # logger.debug(f"{user_shared_objects=}")
    # file_overview.shared_objects = user_shared_objects
    
    # logger.debug(f"{type(group_shared_trees)=}")
    # logger.debug(f"{group_shared_trees=}")
    # file_overview.group_shared_objects = group_shared_trees

    
    # logger.debug(file_overview)
    
    return file_overview
 # def _build(obj):
    #     return (
    #         build_tree(db, user.id, obj)
    #         if isinstance(obj, models.Directory) else
    #         schemas.File.model_validate(obj)
    #     )
    # def _build(obj):
    #     if isinstance(models.Directory):
    #         return schemas.Directory.model_validate(user.root)

    
def add_user_to_group(db: Session, group_id: int, user_id: int):
    group = get_group(db, group_id)
    user = get_user(db, user_id)
    if user in group.members:
        return DuplicateError("Membership already exists")
    group.members.append(user)
    db.commit()
    return group
    
    
def change_user_quota(db: Session, user_id: int, new_quota: int) -> models.User:
    user = get_user(db, user_id)
    if user.used > new_quota:
        raise ValueError("new_quota cant be smaller than users quote")
    user.quota = new_quota
    db.commit()
    return user


def build_tree(db: Session, user_id: int, root: models.StorageObject):
    permission = get_permission_for_user_and_object(db, user_id, root.id)
    base_dict = dict(owner=root.owner, permission=permission)
    
    root_dict = root.to_dict()
    root_dict.update(base_dict)
    
    if isinstance(root, models.File):
        return schemas.SharedFile(**root_dict)
    
    root_children = root.children
    tree = schemas.SharedDirectory(**root_dict) #, children=[])
    
    if not root_children:
        return tree
   
    working_set = collections.deque(itertools.product(root_children, [tree]))
    
    
    def _update(parent: schemas.SharedDirectory, children: list[models.StorageObject]):
        if not children:
            return
        files = [
            schemas.SharedFile(
                **c.to_dict(),
                **base_dict
            )
            for c in children
            if isinstance(c, models.File)
        ]
        directories = [
            c for c in children
            if isinstance(c, models.Directory)
        ]
        parent.children.extend(files)
        if directories:
            working_set.extend(itertools.product(directories, [parent]))
            
    parent: schemas.SharedDirectory = None
    current: models.Directory
    
    while working_set:
        current, parent = working_set.popleft()
        build_args = dict(**current.to_dict(), **base_dict)# children=[])
        print("build args", build_args)
        if isinstance(current, models.File):
            new_node = schemas.SharedFile.model_validate(build_args)
        else:
            new_node = schemas.SharedDirectory.model_validate(build_args)
            _update(new_node, current.children)
        parent.children.append(new_node)
    
    return tree


def init_admin(db: Session):
    create_admin = lambda : create_user(
        db, auth.settings.app_admin_name, auth.get_password_hash(auth.settings.app_admin_pw),
        quota=auth.settings.app_admin_quota_mb * 1024 ** 2, max_objects_per_dir=auth.settings.app_admin_max_objects_per_dir
    )
    try:
        create_admin()
    except DuplicateError as e:
        logger.error(e)
        if auth.settings.app_force_create_admin:
            logger.info("refreshing admin")
            admin = get_user_by_username(db, auth.settings.app_admin_name)
            delete_user(db, admin.id)
            create_admin()

