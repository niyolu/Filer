// import React Hooks
import React from 'react';
import { json, redirect, useSearchParams } from 'react-router-dom';
import queryString from "query-string";
// import components
//import { Modal, ModalBody, ModalHeader } from 'react-bootstrap';
import { setAuthToken } from '../util/auth';
import LoginForm from '../components/forms/LoginForm';
import SignupForm from '../components/forms/SignupForm';
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
        isLogin ? <LoginForm /> : <SignupForm />
    )
};

export default AuthPage;

// action for a post request, to login or signup a user.
export async function action({ request, params }) {
    // await form data...
    const data = await request.formData();
    let loginData


    // create user object
    let user = {
        username: data.get('username'),
        password: data.get('password')
    };

    // check and set mode
    const searchParams = new URL(request.url).searchParams;
    let mode = searchParams.get('mode');
    console.log(mode)
    if (mode !== 'signup' && mode !== 'login') {
        mode = 'signup';
    }

    // add extra fields, if mode is 'signup'
    if (mode === 'signup') {
        user.email = data.get('email');
        let signUpData = await signUp(user)
        console.log(signUpData)
    }

    loginData = await logIn(user)
    console.log(loginData.userData.access_token)

    // login/signup successful
    setAuthToken(
        loginData.userData.access_token,
        30
    );
    return redirect('/');
}

async function signUp(user) {
    console.log(user)
    // send post request...
    const response = await fetch(
        `http://localhost:8000/users`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "username": user.username,
                "password": user.password,
                "is_active": true,
                "quota": 0,
                "used": 0
            })
        }
    );

    // handle response
    if (response.status !== 200) {
        // redirect to error page
        return json({ message: 'Could not fetch userData...' }, { status: response.status });
    } else {
        // return learnunits
        const userData = await response.json();
        return {
            userData: userData,
        };
    }
}

async function logIn(user) {
    console.log(user)
    // send post request...
    const response = await fetch(
        `http://localhost:8000/token`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: queryString.stringify({
                "username": user.username,
                "password": user.password
            })
        }
    );

    // handle response
    if (response.status !== 200) {
        // redirect to error page
        return json({ message: 'Could not fetch userData...' }, { status: response.status });
    } else {
        // return learnunits
        const promise = await response.json();


        return {
            userData: promise,
        };
    }
}