// import react hooks
import React, { useCallback, useState } from 'react';
import { Form, Link, useNavigation } from 'react-router-dom';
import useInput from '../../hooks/use-input';
//import { validateEmail, validatePassword } from './validator';

/**
 * Form component to create a new user.
 * Redirects to home page, after a successful registration.
 *
 * @returns form to signup as a new user
 */
const AuthForm = () => {
    // set submitting status
    const navigation = useNavigation();
    const isSubmitting = navigation.state === 'submitting';

    const [enteredUserName, setEnteredUserName] = useState('');
    const [enteredEmail, setEnteredEmail] = useState('');
    const [enteredPassword, setEnteredPassword] = useState('');
    //const [enteredConfirmPassword, setEnteredConfirmPassword] = useState('');

    // handle change of value
    const userNameChangeHandler = (event) => {
        setEnteredUserName(event.target.value);
    };
    const emailChangeHandler = (event) => {
        setEnteredEmail(event.target.value);
    };
    const passwordChangeHandler = (event) => {
        setEnteredPassword(event.target.value);
    };
    /*
    const confirmPasswordChangeHandler = (event) => {
        setEnteredConfirmPassword(event.target.value);
    };
    */

    // returns a signup form
    return (
        <Form className="m-0 p-0" method="post">
            <div className="pt-3 pb-2 ms-4 pe-4">
                {/* username */}
                <label className="p-0 m-0" htmlFor="username">
                    {'Benutzername'}
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
                {/* Email */}
                <label className="mt-2" htmlFor="email">
                    {'Email'}
                </label>
                <input
                    id="email"
                    name="email"
                    type="text"
                    required
                    placeholder={'beispiel@mail.de'}
                    value={enteredEmail}
                    onChange={emailChangeHandler}
                />
                {/* Password */}
                <label className="mt-4" htmlFor="password">
                    {'Password'}
                </label>
                <input
                    id="password"
                    name="password"
                    type="password"
                    required
                    defaultValue={''}
                    value={enteredPassword}
                    onChange={passwordChangeHandler}
                />
                {/* Password confim
                <input
                    className={`form-control mt-2 ${
                        passwordConfirmHasError
                            ? 'is-invalid'
                            : passwordConfirmIsValid && passwordIsValid
                            ? ' is-valid'
                            : ''
                    }`}
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    required
                    placeholder={'Password bestätigen'}
                    value={enteredPasswordConfirm}
                    onChange={passwordConfirmChangeHandler}
                    onBlur={passwordConfirmBlurHandler}
                />
                {passwordConfirmHasError && <p className="text-danger">{'Passwörter stimmen nicht überein.'}</p>}
                 */}
            </div>
            {/* card footer */}
            <div className="d-flex modal-footer mt-4 pt-2 pb-2">
                {/* switch to login form */}
                <div className="col-auto me-auto">
                    <Link className="btn btn-outline-secondary" to={`?mode=login`}>
                        {'Anmelden'}
                    </Link>
                </div>
                {/* submit form */}
                <div className="col-auto ms-auto">
                    <button className="btn btn-outline-primary" type="submit" disabled={isSubmitting}>
                        {'Registrieren'}
                    </button>
                </div>
            </div>
        </Form>
    );
};

export default AuthForm;
