// import react hooks
import { useRouteError } from 'react-router-dom';

/**
 *
 * @returns
 */
function ErrorPage() {
    const error = useRouteError();

    let title = 'error occurred!';
    let message = 'Something went wrong!';

    if (error.status === 500) {
        message = error.data.message;
    }

    if (error.status === 404) {
        title = 'Not found!';
        message = 'Could not find requested ressource or page!';
    }

    return (
        <div className="main">
            <div className="error-page">
                <h1>{`${error.status || 'Unknown'}: ${title}`}</h1>
                <p>{message}</p>
            </div>
        </div>
    );
}

export default ErrorPage;
