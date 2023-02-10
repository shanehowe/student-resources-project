import { Link, Navigate } from "react-router-dom";
import Proptypes from 'prop-types';
import { Notification } from "./Notification";
import { useState } from "react";
import signUpService from "../services/signup";

export function SignupForm({
    message, isError, notify
}) {
    const [signUpEmail, setSignUpEmail] = useState("");
    const [signUpUsername, setSignUpUsername] = useState("");
    const [signUpFullName, setSignUpFullName] = useState("");
    const [signUpPassword, setSignUpPassword] = useState("");
    const [signUpPasswordConfirm, setSignUpPasswordConfirm] = useState("");
    const [accountCreated, setAccountCreated] = useState(false);

    const handleSignUpEmailChange = ({ target }) => {
        setSignUpEmail(target.value);
    };

    const handleSignUpUsernameChange = ({ target }) => {
        setSignUpUsername(target.value);
    };

    const handleSignUpFullNameChange = ({ target }) => {
        setSignUpFullName(target.value);
    };

    const handleSignUpPasswordChange = ({ target }) => {
        setSignUpPassword(target.value);
    };

    const handleSignUpPasswordConfirmChange = ({ target }) => {
        setSignUpPasswordConfirm(target.value);
    };

    const signUpUser = async (e) => {
        e.preventDefault();
        try {

            if (signUpPassword !== signUpPasswordConfirm) {
                notify("Passwords do not match!", true);
                return;
            }
            await signUpService.signUp(
                signUpEmail, signUpPassword, signUpUsername, signUpFullName
            );
            setAccountCreated(true);
            setSignUpEmail("");
            setSignUpUsername("");
            setSignUpFullName("");
            setSignUpPassword("");
            setSignUpPasswordConfirm("");

            notify("Your account was created. Log in to continue!", false);
            setTimeout(() => {
                setAccountCreated(false);
            }, 100);

        } catch (error) {
            if (error.response.data.detail) {
                const errorMessage = error.response.data.detail;
                notify(errorMessage, true);
            } else {
                notify("An error occurred. Please try again.", true);
            }
        }
    };

    const extraPadding = {
        padding: "20px"
    };
    return (
        <div className="sign-up-container">
            {accountCreated && <Navigate replace to="/login" />}
            <h2>Sign up for an account</h2>
            {message && <Notification message={message} isError={isError} />}
            <form onSubmit={signUpUser}>
                <div>
                    <label>Email</label><br />
                    <input
                        type="text"
                        value={signUpEmail}
                        name="Email"
                        onChange={handleSignUpEmailChange}
                        autoComplete="off"
                        required />
                </div>
                <div>
                    <label>Username</label><br />
                    <input
                        type="text"
                        value={signUpUsername}
                        name="Username"
                        onChange={handleSignUpUsernameChange}
                        autoComplete="off"
                        required />
                </div>
                <div>
                    <label>Full Name</label><br />
                    <input
                        type="text"
                        value={signUpFullName}
                        name="Username"
                        onChange={handleSignUpFullNameChange}
                        autoComplete="off"
                        required />
                </div>
                <div>
                    <label>Password</label><br />
                    <input
                        type="password"
                        value={signUpPassword}
                        name="Password"
                        onChange={handleSignUpPasswordChange}
                        autoComplete="off"
                        required />
                </div>
                <div>
                    <label>Confirm Password</label><br />
                    <input
                        type="password"
                        value={signUpPasswordConfirm}
                        name="PasswordConfirmation"
                        onChange={handleSignUpPasswordConfirmChange}
                        autoComplete="off"
                        required />
                </div>
                <button type="submit">Sign Up</button>
                <div style={extraPadding}>
                    <Link className="form-link" to="/login">Already have an account? Log in here.</Link>
                </div>
            </form>
        </div>
    );
}

SignupForm.propTypes = {
    message: Proptypes.string,
    isError: Proptypes.bool.isRequired,
    notify: Proptypes.func.isRequired
};