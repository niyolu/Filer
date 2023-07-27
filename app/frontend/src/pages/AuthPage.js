// import React Hooks
import React from 'react';
import { json, redirect, useSearchParams } from 'react-router-dom';
// import components
//import { Modal, ModalBody, ModalHeader } from 'react-bootstrap';
import { setAuthToken } from '../util/auth';
import LoginForm from '../components/forms/LoginForm';
//import SignupForm from '../components/forms/SignupForm';

/**
 * Authentication page to login or signup as an admin.
 * Uses url parameter to set mode to login or signup
 * and load the requested form.
 *
 * @returns authentication component
 */
const AuthPage = () => {
    // get and check mode
    const [searchParams] = useSearchParams();
    const isLogin = searchParams.get('mode') === 'login';

    // renders a login/signup form
    /*return (
        <Modal show={true} className="auth-form m-0 p-0">
            <ModalHeader className="ms-0 p-2 ps-3 pe-3">
                <p className="fs-4 m-0 p-0">{isLogin ? 'Login' : 'Registrieren'}</p>
            </ModalHeader>
            <ModalBody className="m-0 p-0">{isLogin ? <LoginForm /> : <SignupForm />}</ModalBody>
        </Modal>
    );*/
    return (
        <LoginForm />
    )
};

export default AuthPage;

// action for a post request, to login or signup a user.
export async function action({ request, params }) {
    // await form data...
    const data = await request.formData();

    // create user object
    let user = {
        email: data.get('email'),
        password: data.get('password')
    };

    // check and set mode
    const searchParams = new URL(request.url).searchParams;
    let mode = searchParams.get('mode');
    if (mode !== 'signup' && mode !== 'login') {
        mode = 'signup';
    }

    // add extra fields, if mode is 'signup'
    if (mode === 'signup') {
        user.username = data.get('username');
        user.passwordConfirm = data.get('confirmPassword');
    }
/*
    // send post request...
    const response = await fetch(
        `${process.env.REACT_APP_ORIGIN_URL_BACKEND}/api/${mode}`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        }
    );

    // // handle errors
    if (response.status === 422 || response.status === 401) {
        return response;
    }
    if (!response.ok) {
        throw json({ message: 'could not authenticate user' }, { status: 500 });
    }

    // parse data
    const resData = await response.json();
    // no admin rights for user
    if (!resData.data.user.isAdmin) {
        throw json({ message: 'not autherized to use application, please contact support' }, { status: 403 });
    }*/
    
    // login/signup successful
    setAuthToken(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0YjRlZGIzYjEzNThjZTQzMDQ1MGZlMiIsImlhdCI6MTY5MDEzMDQzMywiZXhwIjoxNjkwMTMyMjMzfQ.I7u50FlDpfIh4kfcp1x0cSJZx8Mu-ZERppOvhdt4Nz8", 
        30
    );
    return redirect('/');
}
