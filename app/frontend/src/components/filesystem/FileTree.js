import React, { useState } from 'react';
import Modal from "react-modal";
import { FileDownloadButton, RemoveItem } from './FileManagement';
import { getAuthToken } from '../../util/auth';

// FolderNode component
function FolderNode({ folder }) {
    const [isModalOpen, setModalOpen] = useState(false);
    const [addedFile, setAddedFile] = useState(false);
    const handleOpenModal = () => {
        setModalOpen(true);
    };
    const handleCloseModal = () => {
        setModalOpen(false);
    };

    let token = getAuthToken()

    console.log(folder.name)
    return (
        <div>
            <strong>{folder.name}</strong><button onClick={handleOpenModal}>...</button>
            <Modal
                isOpen={isModalOpen}
                onRequestClose={handleCloseModal}
                contentLabel="Example Modal"
            >
                <button onClick={handleCloseModal}>Close</button>
                <h4>Folder: {folder.name}</h4>

                <button onClick={async () => {
                    const response = fetch('http://127.0.0.1:8000/storage/directory', {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'multipart/form-data'
                        },
                        body: {
                            "path": "/",
                            "name": "NEWDir"
                        }
                    });

                    if (!response.ok) {
                        throw new Error('Failed to upload file.' + response);
                    }

                    const data = response.json();
                    console.log(data);
                }}>Add Folder</button>
                <form action={`http://127.0.0.1:8000/storage/file?path=%2F`} method="post" enctype="multipart/form-data">
                    <input type="file" name="file" />
                    <input type='hidden' id='token-input' name='token' />
                    <button onClick={() => {
                        const fileInput = document.getElementById('file-input');
                        const file = fileInput.files[0];

                        // Get the authentication token from localStorage
                        const token = localStorage.getItem('authToken');
                        if (!token) {
                            console.error('Authentication token not found.');
                            return;
                        }

                        // Construct the headers with the token and Content-Type for file upload
                        const headers = new Headers();
                        headers.append('Authorization', `Bearer ${token}`);
                        headers.append('Content-Type', 'multipart/form-data'); // Set the correct Content-Type

                        // Create a FormData object to send the file
                        const formData = new FormData();
                        formData.append('file', file);

                        const options = {
                            headers: {
                                Authorization: "Bearer " + token,
                            }
                        };
                        let url = `http://127.0.0.1:8000/storage/file?path=%2F`

                        fetch(url, options)
                            .then(res => res.json())
                            .then(data => console.log(data));

                    }}>Submit</button>
                </form>




                <RemoveItem fileUrl={`http://127.0.0.1:8000/storage`} fileName={folder.name} path={"/"} />
                <button>Share Folder</button>
            </Modal>
            <ul>
                {folder.children.map((item) => (
                    <li key={item.name}>
                        {item.children ? (
                            <FolderNode folder={item} />
                        ) : (
                            <FileNode file={item} />
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
}

// FileNode component
function FileNode({ file }) {

    const [isModalOpen, setModalOpen] = useState(false);
    const handleOpenModal = () => {
        setModalOpen(true);
    };
    const handleCloseModal = () => {
        setModalOpen(false);
    };
    return (
        <div>
            <span>{file.name}</span>
            <button onClick={handleOpenModal}>...</button>
            <Modal
                isOpen={isModalOpen}
                onRequestClose={handleCloseModal}
                contentLabel="Example Modal"
            >
                <button onClick={handleCloseModal}>Close</button>
                <h4>File: {file.name}</h4>

                <h5>Permissons:</h5>

                <RemoveItem fileUrl={`http://127.0.0.1:8000/storage`} fileName={file.name} path={"/"} />
                <button>Share File</button>
                <FileDownloadButton fileUrl={`http://127.0.0.1:8000/storage/download`} fileName={file.name} path={"/"} />
            </Modal>
        </div>
    );
}

// FileTree component
function FileTree({ data }) {
    return (
        <div>
            <h1>File Tree</h1>
            <FolderNode folder={data} />
        </div>
    );
}

export default FileTree;
