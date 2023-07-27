import React from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import { useLoaderData } from 'react-router-dom';
import FileManagement from '../components/filesystem/FileManagement';


const FilePage = () => {
    const data = useLoaderData();
    console.log(data.fileData)
    return (
        <div>
            <button><Link to="/">Go back to Home</Link></button>
            <h2>File Management</h2>
            <FileManagement data={data.fileData.directory} path={data.fileData.path} />
        </div>
    );
};

export default FilePage;