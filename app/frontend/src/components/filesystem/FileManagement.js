import { Outlet } from "react-router-dom"

import React from "react";

const DirectoryComponent = ({ data, path }) => {
    //console.log(data.filter((item) => typeof item === "string"))
    //console.log(data)
    let array = []
    //console.log(Array.isArray(data))
    const renderFiles = (files) => {
        //console.log("files" + files)
        return (
            <ul>
                {files.map((file, index) => (
                    <li key={index}>{file}</li>
                ))}
            </ul>
        );
    };

    const renderSubdirectories = (directories) => {
        //console.log("directories" + directories)
        return (
            <ul>
                {directories.map((dir, index) => {
                    //console.log(dir)
                    return (
                        <li key={index}>
                            {dir.directory ? (
                                <DirectoryComponent data={dir.directory} path={`${path}/${dir.name}`} />
                            ) : null}
                        </li>
                    )
                })}
            </ul>
        );
    };
    
    return (
        <div>
            <h3>Current Path: {path}</h3>
            {
                Array.isArray(data) ? 
                renderFiles(data.filter((item) => typeof item === "string")) : 
                renderFiles(data.directory)
            }
            {
                Array.isArray(data) ? 
                renderSubdirectories(data.filter((item) => typeof item === "object")) : 
                null
            }
        </div>
    );
};

export default DirectoryComponent;



/*export default function FileManagement({ fileData }) {
    console.log(fileData.directory)
    let displayTree = fileData.directory.map((dir, key) => {
        console.log(dir)
        return (
            <div>
                <h1>{dir.name}</h1>

                <Outlet />
            </div>
        )
    })
    return (
        <div>
            <h4>Dein Filetree</h4>
            {displayTree}
        </div>
    )
}*/