import { Link,  useNavigate } from "react-router-dom";
import { Notification } from "./Notification";
import { useState } from "react";
import { useAuth } from "./AuthProvider";

export function LoginForm ({
 message, isError, notify
}) {

    const [logInUsername, setLogInUsername] = useState("");
    const [logInPassword, setLogInPassword] = useState("");
    let navigate = useNavigate();
    let auth = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await auth.handleLogin(logInUsername, logInPassword);
            navigate("/resource-center", { replace: true });
        } catch (error) {
            notify("Incorrect username/password. If you need to recover your account, contact the apps admin", true);
        }
        
    }

    return (
        <div className="log-in-container">
            <h2>Log in</h2>
            {message && <Notification message={message} isError={isError} />}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username</label><br />
                    <input
                        type="text"
                        value={logInUsername}
                        name="Username"
                        autoComplete="off"
                        onChange={({ target }) => setLogInUsername(target.value)}
                        required />
                </div>
                <div>
                    <label>Password</label>
                    <br />
                    <input
                        type="password"
                        value={logInPassword}
                        name="Password"
                        autoComplete="off"
                        onChange={({ target }) => setLogInPassword(target.value)}
                        required />
                </div>
                <div>
                    <button type="submit">Login</button>
                </div>

                <div>
                    <Link className="form-link" to="/signup">Don't have an account? Sign up here.</Link>
                </div>
            </form>

        </div>
    );
}