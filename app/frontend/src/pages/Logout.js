import { redirect } from 'react-router-dom';

// action to trigger a logout
export function action() {
    localStorage.removeItem('mca_token');
    localStorage.removeItem('mca_expiration');
    return redirect('/auth?mode=login');
}
