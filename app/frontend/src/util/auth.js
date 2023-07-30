// import React Hooks
import { redirect } from 'react-router-dom';

/**
 * save token to local storage (successful login).
 *
 * @param {*} token to be stored
 * @param {*} duration token's expiration date
 */
export function setAuthToken(token, duration) {
    // store token
    localStorage.setItem('mca_token', token);
    // store token's expiration
    setTokenExpiration(duration);
}

/**
 * saves token's expiration date to local storage
 *
 * @param {*} duration token's lifetime
 */
export function setTokenExpiration(duration) {
    // set and store and expiration time
    const expiration = new Date();
    expiration.setMinutes(expiration.getMinutes() + parseInt(duration));
    localStorage.setItem('mca_expiration', expiration.toISOString());
}

/**
 * Get remaining token duration, token is expired if < 0
 *
 * @returns remaining time
 */
export function getTokenDuration() {
    // get duration time
    const expirationDate = localStorage.getItem('mca_expiration');
    if (expirationDate === null) {
        return null;
    }
    if (expirationDate === 'EXPIRED') {
        removeAuthToken()
    }
    const tokenExpiration = new Date(expirationDate);
    // check for current remaining time
    const now = new Date();
    const duration = tokenExpiration.getTime() - now.getTime();

    console.log(duration)

    return duration;
}

/**
 * Get token from local storage, null if does not exist. Checks exparation.
 *
 * @returns token from local storage, null if none, 'EXPIRED' if not longer valid
 */
export function getAuthToken() {
    // get and check token
    const token = localStorage.getItem('mca_token');
    if (!token) {
        return null;
    }
    // get and check token's expiration time
    const tokenDuration = getTokenDuration();
     if (tokenDuration < 0 || tokenDuration === null) {
        return 'EXPIRED';
    }

    return token;
}

// remove token from local storage (logout)
export function removeAuthToken() {
    localStorage.removeItem('mca_token');
}

/**
 * Loader function for routes.
 * @returns token
 */
export function tokenLoader() {
    return getAuthToken();
}

// get token from storage
export function getToken() {
    const token = localStorage.getItem('mca_token');
    return token;
}

/**
 * Check if user is logged in, redirect if not.
 *
 * @returns redirect or null
 */
export function checkAuthLoader() {
    const token = getAuthToken();
    if (!token || null) {
        return redirect('/auth?mode=login');
    }
    return null;
}
