import { getAuthToken, setAuthToken } from '../util/auth';
import { json, redirect } from 'react-router-dom';
import mov from '../files/realshort.mp4'
import txt from '../files/File.txt'
import img from '../files/Happy Pants Guy__an__r2x.png'

export async function homeLoader() {
    const token = getAuthToken();
    if (!token || null) {
        return redirect('/auth?mode=login');
    }
    return null
}

export async function userLoader() {
    const token = getAuthToken();
    if (!token || null) {
        //token = setAuthToken()
        return redirect('/auth?mode=login');
    }

    const response = await fetch(`http://localhost:8000/users/me`, {
        method: 'get',
        headers: {
            accept: "application / json",
            Authorization: "Bearer " + token
        }
    });

    // handle response
    if (response.status !== 200) {
        // redirect to error page
        return json({ message: 'Could not fetch data1...' }, { status: response.status });
    } else {
        // return learnunits
        const userData = await response.json();
        console.log(userData)

        const allUser = await getAllUsers(token)
        const allGroups = await getAllGroups(token)
        const myGroups = await getMyGroups(token)
        return {
            userData: userData,
            groupData: myGroups,
            allUserData: allUser,
            allGroupData: allGroups
        }
    }
}

async function getAllUsers(token) {
    const response = await fetch(`http://localhost:8000/users`, {
        method: 'get',
        headers: {
            accept: "application / json",
            Authorization: "Bearer " + token
        }
    });

    // handle response
    if (response.status !== 200) {
        // redirect to error page
        return json({ message: 'Could not fetch data2...' }, { status: response.status });
    } else {
        // return learnunits
        const userData = await response.json();
        console.log(userData)

        return userData
    }
}
async function getAllGroups(token) {
    const response = await fetch(`http://localhost:8000/groups/groups`, {
        method: 'get',
        headers: {
            accept: "application / json",
            Authorization: "Bearer " + token
        }
    });

    // handle response
    if (response.status !== 200) {
        // redirect to error page
        return json({ message: 'Could not fetch data3...' }, { status: response.status });
    } else {
        // return learnunits
        const groupData = await response.json();
        console.log(groupData)

        return groupData
    }
}
async function getMyGroups(token) {
    const response = await fetch(`http://localhost:8000/groups/me`, {
        method: 'get',
        headers: {
            accept: "application / json",
            Authorization: "Bearer " + token
        }
    });

    // handle response
    if (response.status !== 200) {
        // redirect to error page
        return json({ message: 'Could not fetch data4...' }, { status: response.status });
    } else {
        // return learnunits
        const groupData = await response.json();
        console.log(groupData)

        return groupData
    }
}

export async function fileDirLoader() {
    let file = {
        directory: [
            {
                name: "Dir1",
                directory: [
                    "file1.xy",
                    "file2.xy",
                    {
                        name: "Dir3",
                        directory: [
                            "file3.xy",
                            "file4.xy",
                        ]
                    },
                    {
                        name: "Dir4",
                        directory: [
                            "file5.xy",
                            "file6.xy",
                            "file7.xy",
                            "file8.xy",
                        ]
                    },
                    {
                        name: "Dir5",
                        directory: [
                            "file9.xy",
                        ]
                    }
                ]
            },
            {
                name: "Dir2",
                directory: [
                    "file10.xy",
                    {
                        name: "Dir6",
                        directory: [
                            "file13.xy",
                            {
                                name: "Dir7",
                                directory: [
                                    "file14.xy",
                                    "file15.xy",
                                ]
                            }
                        ]
                    },
                    "file16.xy",
                    "file17.xy",
                    "file18.xy",
                    "file19.xy",
                    "file20.xy",
                ]
            },
        ],
        path: "xy/123"
    };
    const token = getAuthToken();
    if (!token || null) {
        //token = setAuthToken()
        return redirect('/auth?mode=login');
    }
    const response = await fetch(`http://localhost:8000/users/me`, {
        method: 'get',
        headers: {
            accept: "application / json",
            Authorization: "Bearer " + token 
        }
    });

    // handle response
    if (response.status !== 200) {
        // redirect to error page
        return json({ message: 'Could not fetch data...' }, { status: response.status });
    } else {
        // return learnunits
        const userData = await response.json();
        console.log(userData)
        const dirData = await dirLoader(token)
        return {
            userData: userData,
            dirData: dirData
        }
    }
    /*return {
        fileData: file
    }*/
}

async function dirLoader(token) {
    const response = await fetch(`http://localhost:8000/storage`, {
        method: 'get',
        headers: {
            accept: "application / json",
            Authorization: "Bearer " + token
        }
    });

    // handle response
    if (response.status !== 200) {
        // redirect to error page
        return json({ message: 'Could not fetch data...' }, { status: response.status });
    } else {
        // return learnunits
        const userData = await response.json();
        console.log(userData)

        return {
            userData: userData
        }
    }
}

export function fileLoader() {
    const token = getAuthToken();
    if (!token || null) {
        //token = setAuthToken()
        return redirect('/auth?mode=login');
    }
    return {
        video: img
    }
}