import React, { useState } from 'react';
import { getAuthToken } from '../../util/auth';
export default function User({ userData, groupData, allGroupData }) {
    console.log(allGroupData)
    const [user, setUser] = useState(userData);

    const [groups, setGroups] = useState(groupData);
    const [selectedUser, setSelectedUser] = useState(1);

    
    
    return (
        <div>
            <div>
                <h4>User Info</h4>
                <table>
                    <tbody>
                        <tr>
                            <th>
                                Username:
                            </th>
                            <td>
                                {userData.username}
                            </td>
                        </tr>
                        <tr>
                            <th>
                                Storage Used:
                            </th>
                            <td>
                                {userData.used} / {userData.quota} Byte
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div>
                <h4>Active Groups</h4>
                {groupData.length <= 0 ? (<div></div>) : (<div>You are not part of any groups</div>)}
            </div>
        </div>
    );
};
