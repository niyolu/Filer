import React, { useState } from 'react';
import { BrowserRouter as Router, Switch, Route, Link, Navigate } from 'react-router-dom';
import { useLoaderData } from 'react-router-dom';
import FileManagement from '../components/filesystem/FileManagement';
import FolderTree, { testData } from 'react-folder-tree';
import { useNavigate } from "react-router-dom";
import Modal from "react-modal";
import Video from '../components/fileTypes/Video';
import Text from '../components/fileTypes/Text';
import Image from '../components/fileTypes/Image';


const FileContentPage = () => {
    let type = ""
    let display = null
    let data = useLoaderData()
    console.log(data)
    switch(type) {
        case "video":
            display = <Video videoUrl={data.video} />;
            break;
        case "text": 
            display = <Text textFile={data} />;
            break;
        default: 
            display = <Image image={data.video} />;
            break;
    }

    
    return (
        <div>
            <button><Link to="../">Go back</Link></button>
            {display}
        </div>
        
    )
}

export default FileContentPage