import React from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import { useLoaderData } from 'react-router-dom';


import User from '../components/user/User'
import Admin from '../components/user/Admin'

const UserPage = () => {
    const data = useLoaderData();    
    console.log(data)
    
    return (
        <div>
            <button><Link to="/">Go back to Home</Link></button>
            <h2>User and Group Management</h2>
            <h3>Users</h3>
            <User userData={data.userData} groupData={data.groupData}/>
            {
                data.userData.username === "root" ?
                    <Admin userData={data.userData} allGroupData={data.allGroupData} allUserData={data.allUserData} /> :
                null
            }
            
        </div>    
    );
};

export default UserPage;

