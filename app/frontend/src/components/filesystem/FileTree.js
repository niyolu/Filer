import React, {useState} from 'react';
import Modal from "react-modal";
import { FileDownloadButton, RemoveItem } from './FileManagement';

// FolderNode component
function FolderNode({ folder }) {
    const [isModalOpen, setModalOpen] = useState(false);
    const handleOpenModal = () => {
        setModalOpen(true);
    };
    const handleCloseModal = () => {
        setModalOpen(false);
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

                <button>Add Folder</button>
                <button>Add File</button>


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
                <FileDownloadButton fileUrl={`http://127.0.0.1:8000/storage/download`} fileName={file.name} path={"/"}/>
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
