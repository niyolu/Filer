// RootLayout.js
import React from 'react';
import { Outlet, Form, useRouteLoaderData, useLoaderData, useSubmit } from 'react-router-dom';

const RootLayout = ({ children }) => {
    const token = useRouteLoaderData('root');
    return (
        <div>
            {/* Add any common elements or components that should appear in the layout */}
            <header>
                {token && (
                    <Form action="/logout" method="post">
                        <button className="nav-link logout">Logout</button>
                    </Form>
                )}
            </header>

            <main>
                {/* The "children" prop contains the component that will be rendered within the layout */}
                {children}
                <Outlet />
            </main>

            <footer>
                {/* Your footer content */}
            </footer>
        </div>
    );
};

export default RootLayout;
