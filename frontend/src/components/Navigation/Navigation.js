import { Link } from "react-router-dom"
import Proptypes from 'prop-types';

import "./Navigation.css"
import { useAuth } from "../AuthProvider";

export function Navigation() {
    const auth = useAuth();
    return (
        <nav className="nav-bar">
            <Link className="nav-item" replace to="/resource-center">Modules</Link>
            <Link className="nav-item" replace to="/python-challenges">Python Challenges</Link>
            <Link className="nav-item" onClick={auth.handleLogout}>Log out</Link>
        </nav>
    );
}

Navigation.prototype = {
    handleLogout: Proptypes.func.isRequired
}