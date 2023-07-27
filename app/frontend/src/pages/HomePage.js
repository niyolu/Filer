import React from 'react';
import { Form, useRouteLoaderData, BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import User from '../components/user/User'

const HomePage = () => {
    return (
        <div>
            <h1>Welcome to File Cloud</h1>
            <p>Share and store your files securely in the cloud.</p>
            <button><Link to="/user">User & Group Management</Link></button>
            <button><Link to="/file">File Management</Link></button>
        </div>
    );
};

export default HomePage;