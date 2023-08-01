import React, { useState } from 'react';
import Modal from "react-modal";
import { FileDownloadButton, RemoveItem } from './FileManagement';
// import { getAuthToken } from '../../util/auth';

// Function to get the authentication token from local storage
function getAuthToken() {
  // Implement the logic to retrieve the authentication token from local storage
  return localStorage.getItem('mca_token');
}

async function uploadFile(file, path, token) {
  const formData = new FormData();
  formData.append('file', file); // Just append the file directly

  const headers = new Headers();
  headers.append('Authorization', `Bearer ${token}`);

  try {
    const response = await fetch(`http://127.0.0.1:8000/storage/file?path=${encodeURIComponent(path)}`, {
      method: 'POST',
      body: formData,
      headers: headers,
    });

    if (!response.ok) {
      throw new Error('Failed to upload file.');
    }

    const result = await response.json();
    console.log('Success:', result);
  } catch (error) {
    console.error('Error:', error);
  }
}


// FolderNode component
function FolderNode({ folder }) {
  const [isModalOpen, setModalOpen] = useState(false);
  //const [addedFile, setAddedFile] = useState(false);
  const handleOpenModal = () => {
    setModalOpen(true);
  };
  const handleCloseModal = () => {
    setModalOpen(false);
  };

  const handleSubmitFolder = async () => {
    const token = getAuthToken();
    if (!token) {
      console.error('Authentication token not found.');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/storage/directory', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "path": "/",
          "name": "NEWDir", // Replace "NEWDir" with the desired folder name
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to add folder.');
      }

      const data = await response.json();
      console.log(data); // You can handle the response data as needed.
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleSubmitFile = async (event) => {
    event.preventDefault();

    const token = getAuthToken();
    if (!token) {
      console.error('Authentication token not found.');
      return;
    }
    
    const fileField = event.target.querySelector('input[type="file"]');
    const file = fileField.files[0];
    const path = folder.path;

    uploadFile(file, path, token);
  };

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

        <button onClick={handleSubmitFolder}>Add Folder</button>
        <form
        //   action={`http://127.0.0.1:8000/storage/file?path=%2F`}
        //   method="post"
          encType="multipart/form-data"
          onSubmit={handleSubmitFile}
        >
          <input type="file" name="file" />
          <input type='hidden' id='token-input' name='token' />
          <button type="submit">Submit</button>
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

        <h5>Permissions:</h5>

        <RemoveItem fileUrl={`http://127.0.0.1:8000/storage`} fileName={file.name} path={file.path} />
        <button>Share File</button>
        <FileDownloadButton fileUrl={`http://127.0.0.1:8000/storage/download`} fileName={file.name} path={file.path} />
      </Modal>
    </div>
  );
}

// FileTree component
function FileTree({ data }) {
  console.log(data)
  return (
    <div>
      <h1>File Tree</h1>
      <FolderNode folder={data} />
    </div>
  );
}

export default FileTree;
