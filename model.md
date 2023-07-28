```mermaid
classDiagram
direction BT
class directories {
   int(11) id
}
class files {
   varchar(255) filetype
   blob content
   int(11) id
}
class group_share {
   varchar(10) permission
   int(11) group_id
   int(11) obj_id
}
class groups {
   varchar(255) name
   int(11) id
}
class storage_share {
   varchar(10) permission
   int(11) user_id
   int(11) obj_id
}
class storageobjects {
   varchar(255) name
   varchar(255) path
   varchar(255) type
   int(11) owner_id
   int(11) parent_id
   int(11) id
}
class user_group_table {
   int(11) user_id
   int(11) group_id
}
class users {
   varchar(255) username
   varchar(255) hashed_password
   tinyint(1) is_active
   bigint(20) quota
   bigint(20) used
   int(11) max_objects_per_dir
   int(11) root_id
   int(11) id
}

directories  -->  storageobjects : id
files  -->  storageobjects : id
group_share  -->  groups : group_id:id
group_share  -->  storageobjects : obj_id:id
storage_share  -->  storageobjects : obj_id:id
storage_share  -->  users : user_id:id
storageobjects  -->  directories : parent_id:id
storageobjects  -->  users : owner_id:id
user_group_table  -->  groups : group_id:id
user_group_table  -->  users : user_id:id
users  -->  directories : root_id:id
```
