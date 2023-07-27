import { getAuthToken, setAuthToken } from '../util/auth';
import { json, redirect } from 'react-router-dom';


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
    let user = [
        { id: 1, name: 'John Doe', email: 'john@example.com', groups: ['Group1', 'Group2'] },
        { id: 2, name: 'Jane Smith', email: 'jane@example.com', groups: ['Group1'] }
    ]
    let group = ['Group1', 'Group2', 'Group3', 'Group4']
    return {
        userData: user,
        groupData: group
    }
}

export async function fileLoader() {
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
                                name: "Dir6",
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
    return {
        fileData: file
    }
}