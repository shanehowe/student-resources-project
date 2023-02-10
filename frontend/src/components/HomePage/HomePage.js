import { Link } from "react-router-dom";

import "./HomePage.css";

export function HomePage() {
    return (
        <div className="home-container">
            <div className="center">
            <h1 id="home-heading">Resource Center</h1>
            <div className="links-container">
                <Link className="home-link" to="/login">Login</Link><br />
                <Link className="home-link" to="/signup">Sign up</Link>
            </div>
            <div className="about-container">
                <h2>What is Resource Center?</h2>
                <p>Resource Center is a web-based tool for students of MTU Kerry studying Computing with Software Development. It provides a platform for students to share links to helpful resources such as study guides, youtube videos, websites, or just about anything they think is helpful for specific modules. Additionally, students can use interactive coding challenges to practice and improve their coding skills all from within the browser.</p>
                
            </div>
            <div className="contributing-container">
                <h2>Interested in contributing?</h2>
                <p>If you are interested in contributing to this project, great! It'd be great to make this a group project where we can all learn new things.</p>
            </div>
            </div>
        </div>
    )
}