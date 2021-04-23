import userLogo from "./user.png";
import './UserInfo.css';

function UserProfile(){

    return (

        <div className='Info-Container'>

            <h3> Welcome, Lena </h3>
            <a>Change Profile</a>
            <img className='info' src={userLogo} alt="logo" />

        </div>

    );
}

export default UserProfile;