import { createContext, useContext, useEffect, useState } from "react";
import loginService from "../services/login";
import resourceServices from "../services/resourcePosts";
import codeServices from "../services/codeSubmission";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null || JSON.parse(localStorage.getItem("LoggedInResourceUser")));

    useEffect(() => {
        const jsonUser = window.localStorage.getItem("LoggedInResourceUser");
        if (jsonUser) {
            const user = JSON.parse(jsonUser);
            resourceServices.setToken(user.token);
            codeServices.setToken(user.token);
        }
    }, []);

    const handleLogin = async (username, password) => {
        const user = await loginService.login(username, password);
        window.localStorage.setItem(
            "LoggedInResourceUser", JSON.stringify(user)
        );
        resourceServices.setToken(user.token);
        codeServices.setToken(user.token);
        setUser(user);
    };

    const handleLogout = (e) => {
        e.preventDefault();
        setUser(null);
        window.localStorage.removeItem("LoggedInResourceUser");
    };

    let value = { handleLogin, handleLogout, user, setUser };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}


export const useAuth = () => {
    return useContext(AuthContext);
}