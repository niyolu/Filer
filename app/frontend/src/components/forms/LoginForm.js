// import react hooks
import React, { useCallback, useState } from 'react';

import { Form, Link, useNavigation } from 'react-router-dom';


/**
 * Login form for confirming user credentials.
 * After successful login redirects to homepage.
 *
 * @returns login form
 */
const AuthForm = () => {
    // set submitting status
    const navigation = useNavigation();
    const isSubmitting = navigation.state === 'submitting';

    const [enteredUserName, setEnteredUserName] = useState('');
    const [enteredPassword, setEnteredPassword] = useState('');

    // handle change of value
    const userNameChangeHandler = (event) => {
        setEnteredUserName(event.target.value);
    };
    const passwordChangeHandler = (event) => {
        setEnteredPassword(event.target.value);
    };

    // login form component
    return (
        <Form className="m-0 p-0" method="post">
            <div className="pt-3 pb-2 ms-4 pe-4">
                {/* UserName */}
                <label className="p-0 m-0" htmlFor="username">
                    {'UserName'}
                </label>
                <input
                    className={`form-control mt-2 m-0`}
                    id="username"
                    name="username"
                    type="text"
                    required
                    placeholder={'KingJulian123'}
                    value={enteredUserName}
                    onChange={userNameChangeHandler}
                />
                {/* Password */}
                <label className="mt-4" htmlFor="password">
                    {'Password'}
                </label>
                <input
                    className={`form-control mt-2 m-0`}
                    id="password"
                    name="password"
                    type="password"
                    required
                    defaultValue={''}
                    value={enteredPassword}
                    onChange={passwordChangeHandler}
                />
            </div>
            {/* form footer */}
            <div className="d-flex modal-footer mt-4 pt-2 pb-2">
                {/* switch to signup form */}
                <div className="col-auto me-auto">
                    <Link className="btn btn-outline-secondary" to={`?mode=signup`}>
                        {'Registrieren'}
                    </Link>
                </div>
                {/* submit form */}
                <div className="col-auto ms-auto">
                    <button className="btn btn-outline-primary" type="submit" disabled={isSubmitting}>
                        {'Anmelden'}
                    </button>
                </div>
            </div>
        </Form>
    );
};

export default AuthForm;
