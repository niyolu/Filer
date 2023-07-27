import React, { useState } from 'react';
export default function User({userData, groupData}) {
    const [users, setUsers] = useState(userData);

    const [groups, setGroups] = useState(groupData);
    const [selectedUser, setSelectedUser] = useState(1);

    const addUserToGroup = (userId, groupName) => {
        setUsers((prevUsers) => {
            const updatedUsers = prevUsers.map((user) => {
                if (user.id === userId) {
                    return { ...user, groups: [...user.groups, groupName] };
                }
                return user;
            });
            return updatedUsers;
        });
    }; 
    const removeUserToGroup = (userId, groupName) => {
        setUsers((prevUsers) => {
            const updatedUsers = prevUsers.map((user) => {
                if (user.id === userId) {
                    console.log(user.groups)
                    let newGroups = user.groups.map((group) => {
                        if(group !== groupName) {
                            return group;
                        }
                    })
                    return { ...user, groups: [newGroups] };
                }
                return user;
            });
            return updatedUsers;
        });
    };

    let selectUser = (userId) => {
        setSelectedUser(userId)
    }
    //console.log(users.find((user) => user.id === selectedUser).id)
    return (
        <div>
            <ul>
                {users.map((user) => (
                    <li key={user.id} onClick={() => selectUser(user.id)}>
                        <strong>{user.name}</strong> ({user.email})
                        <ul>
                            {user.groups.map((group) => (
                                <li key={group}>{group}</li>
                            ))}
                        </ul>
                    </li>
                ))}
            </ul>
            <h3>Groups</h3>
            <ul>
                {groups.map((group) => (
                    <li key={group}>
                        {group}
                        <button onClick={() => addUserToGroup(users.find((user) => user.id === selectedUser).id, group)}>
                            Add {users.find((user) => user.id === selectedUser).name}
                        </button>
                        <button onClick={() => removeUserToGroup(users.find((user) => user.id === selectedUser).id, group)}>
                            Add {users.find((user) => user.id === selectedUser).name}
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
};
