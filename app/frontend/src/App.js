import React from 'react'
import { createBrowserRouter, RouterProvider} from 'react-router-dom'

import RootLayout from './pages/RootLayout';
import ErrorPage from './pages/ErrorPage';
import AuthPage, { action as authAction } from './pages/AuthPage';
import { action as logoutAction } from './pages/Logout';

import { tokenLoader, checkAuthLoader } from './util/auth';
import { fileLoader, homeLoader, userLoader } from './util/loader';
import HomePage from './pages/HomePage';
import UserPage from './pages/UserPage';
import FilePage from './pages/FilePage';


const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    id: 'root',
    loader: tokenLoader,
    children: [
      {
        index: true,
        id: 'home',
        element: <HomePage />,
        loader: homeLoader
      },
      // authentication
      {
        path: 'auth',
        element: <AuthPage />,
        action: authAction
      },
      // logout action
      {
        path: 'logout',
        action: logoutAction
      },
      {
        path: '',
        loader: checkAuthLoader,
        children: [
          {
            path: 'user',
            loader: checkAuthLoader,
            children: [
              {
                index: true,
                id: 'userpage',
                element: <UserPage />,
                loader: userLoader
              },
            ]
          },
          {
            path: 'file',
            loader: checkAuthLoader,
            children : [
              {
                index: true,
                id: 'filemanagement',
                element: <FilePage />,
                loader: fileLoader
              }
            ]
          }
        ]
      }
    ]
  }
])


function App() {
  return <RouterProvider router={router} />
}

export default App;