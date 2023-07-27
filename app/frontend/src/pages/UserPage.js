import React from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import { useLoaderData } from 'react-router-dom';


import User from '../components/user/User'

const UserPage = () => {
    const data = useLoaderData();    
    console.log(data)
    
    return (
        <div>
            <button><Link to="/">Go back to Home</Link></button>
            <h2>User and Group Management</h2>
            <h3>Users</h3>
            <User userData={data.userData} groupData={data.groupData} />
        </div>    
    );
};

export default UserPage;

