import React, { useState } from 'react';
import { BrowserRouter as Router, Switch, Route, Link, Navigate } from 'react-router-dom';
import { useLoaderData } from 'react-router-dom';
import FileManagement from '../components/filesystem/FileManagement';
import FolderTree, { testData } from 'react-folder-tree';
import { useNavigate } from "react-router-dom";
import Modal from "react-modal";
import FileTree from '../components/filesystem/FileTree';



const FilePage = () => {
    const data = useLoaderData();
    console.log(data)
    const [dirData, setDirData] = useState(data.userData);
    const [isModalOpen, setModalOpen] = useState(false);
    const [selectedUser, setSelectedUser] = useState("");
    const [selectedGroup, setSelectedGroup] = useState("");
    const [selection, setSelection] = useState("user");

    const handleOpenModal = () => {
        setModalOpen(true);
    };
    const handleCloseModal = () => {
        setModalOpen(false);
    };
    function handledirData(newData) {
        setDirData(newData)
    };
    const handleSubmit = () => {
        console.log("Submit")
    };
    let folder = getFolder(dirData)
    const navigate = useNavigate();

    const onTreeStateChange = (state, event) => {
        console.log(state, event)
    }
    const onNameClick = ({ defaultOnClick, nodeData }) => {
        defaultOnClick();
    };
    const FileIcon = () => {
        const handleClick = () => {
            //navigate("../user")
            navigate("xyz")
        };
        return (
            <svg onClick={handleClick} xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark" viewBox="0 0 16 16">
                <path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z" />
            </svg>
        )
    };

    const handleSelectGroupChange = (event) => {
        const selectedOption = event.target.value;
        setSelectedGroup(selectedOption);
    }; 
    const handleSelectUserChange = (event) => {
        const selectedOption = event.target.value;
        setSelectedUser(selectedOption);
    };
    return (
        <div>
            <button><Link to="/">Go back to Home</Link></button>
            <h2>File Management</h2>
            <button onClick={handleOpenModal}>Share Files or Directories</button>
            <Modal
                isOpen={isModalOpen}
                onRequestClose={handleCloseModal}
                contentLabel="Example Modal"
            >
                <button onClick={handleCloseModal}>Close</button>
                <h2>Share File</h2>
                <p>Share with User or Group</p>
                <button onClick={() => { setSelection("user") }}>User</button>
                <button onClick={() => { setSelection("group") }}>Group</button>
                {
                    selection === "user" ? (
                        <div>
                            <p>Share with User:</p>
                            <select value={selectedGroup} onChange={handleSelectUserChange}>
                                <option value="">Select a target user</option>
                                {
                                    folder.map((item, key) => {
                                        return (
                                            <option value={item.name}>{item.name}</option>
                                        )
                                    })
                                }
                            </select>
                        </div>
                    ) : (
                        <div>
                            <p>Share with Group:</p>
                                <select value={selectedGroup} onChange={handleSelectGroupChange}>
                                <option value="">Select a target group</option>
                                {
                                    folder.map((item, key) => {
                                        return (
                                            <option value={item.name}>{item.name}</option>
                                        )
                                    })
                                }
                            </select>
                        </div>
                    )
                }

                {
                    selection === "user" ? (<p>Selected User is {selectedUser}</p>) : (<p>Selected Group is {selectedGroup}</p>)
                }
                
                <button onClick={handleSubmit}>Submit</button>

            </Modal>
            <FileTree data={testData} />
            
            
        </div>
    );
};

function getFolder(dir, path = [], pathIndex = 0) {
    const result = [];

    if (Array.isArray(dir)) {
        dir.forEach((item, index) => {
            if (typeof item !== 'string') {
                const newPath = [...path, index];
                result.push({
                    name: item.name,
                    path: newPath
                });
                result.push(...getFolder(item.directory, newPath));
            }
        });
    }

    return result;

}


export default FilePage;