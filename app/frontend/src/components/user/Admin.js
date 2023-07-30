import React, { useState } from 'react';
import Modal from "react-modal";
import { getAuthToken } from '../../util/auth';
export default function Admin({userData, groupData, allGroupData, allUserData}) {
    const [users, setUsers] = useState(userData);
    const [selectedUser, setSelectedUser] = useState("");
    const [isModalOpen, setModalOpen] = useState(false);
    const [isModalOpenGroups, setModalOpenGroups] = useState(false);
    const [enteredGroupname, setEnteredGroupname] = useState("");
    const [selectedGroup, setSelectedGroup] = useState("");

    const handleOpenModal = () => {
        setModalOpen(true);
    };
    const handleCloseModal = () => {
        setModalOpen(false);
    };

    const handleOpenModalGroups = (name) => {
        setModalOpenGroups(true);
        setSelectedGroup(name)
    };
    const handleCloseModalGroups = () => {
        setModalOpenGroups(false);
    };

    const groupnameChangeHandler = (event) => {
        setEnteredGroupname(event.target.value);
        console.log(enteredGroupname)
    };

    console.log(selectedUser)

    async function handleCreate() {
        let token = getAuthToken()
        await fetch(
            `http://localhost:8000/groups/?group_name=${enteredGroupname}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': "Bearer " + token
                }
            }
        ).then((response) => response.json())
        .then((json) => {console.log(json)})
        setModalOpen(false)
    }

    console.log(selectedUser)

    async function handleCommit() {
        let token = getAuthToken()
        await fetch(
            `http://localhost:8000/groups/join?group_name=${selectedGroup}&user_name=${selectedUser}`,
            {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': "Bearer " + token
                }
            }
        ).then((response) => response.json())
        .then((json) => { console.log(json) })
        //location.reload();
    }

    /*const addUserToGroup = (userId, groupName) => {
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
    };*/

    let handleSelectedUserChange = (event) => {
        const selectedOption = event.target.value;
        setSelectedUser(selectedOption);
    }
    //console.log(users.find((user) => user.id === selectedUser).id)

    return (
        <div>
            <button onClick={handleOpenModal}>Create Group</button>
            <Modal
                isOpen={isModalOpen}
                onRequestClose={handleCloseModal}
                contentLabel="Example Modal"
            >
                <button onClick={handleCloseModal}>Close</button>
                <h4>Create Group</h4>
                <table>
                    <tbody>
                        <tr>
                            <th>Groupname:</th>
                            <td>
                                <input
                                    className={`form-control mt-2`}
                                    id="groupname"
                                    name="groupname"
                                    type="text"
                                    required
                                    defaultValue={''}
                                    value={enteredGroupname}
                                    onChange={groupnameChangeHandler}
                                />    
                            </td>
                        </tr>
                    </tbody>
                </table>
                <button onClick={handleCreate}>Create</button>
            </Modal>

            <div>
                <h4>Available Groups</h4>
                <ul>
                    {
                        allGroupData.map((group) => {
                            console.log(group)
                            return (
                                <li>{group.name} <button onClick={() => { handleOpenModalGroups(group.name) }}>...</button></li>
                            )
                        })
                    }
                </ul>
            </div>
            <Modal
                isOpen={isModalOpenGroups}
                onRequestClose={handleOpenModalGroups}
                contentLabel="Example Modal"
            >
                <button onClick={handleCloseModalGroups}>Close</button>
                <h4>Add to group</h4>
                <select value={selectedUser} onChange={handleSelectedUserChange}>
                    <option value="">Select a target user</option>
                    {
                        allUserData.map((item, key) => {
                            console.log(item)
                            return (
                                <option value={item.username}>{item.username}</option>
                            )
                        })
                    }
                </select>
                <button onClick={() => { handleCommit() }}>Add</button>
            </Modal>
            {/*
            <ul>
                {users ? users.map((user) => (
                    <li key={user.id} onClick={() => selectUser(user.id)}>
                        <strong>{user.name}</strong> ({user.email})
                        <ul>
                            {user.groups.map((group) => (
                                <li key={group}>{group}</li>
                            ))}
                        </ul>
                    </li>
                )) : (<div>No users available</div>)}
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
            </ul>*/}
        </div>
    );
};
