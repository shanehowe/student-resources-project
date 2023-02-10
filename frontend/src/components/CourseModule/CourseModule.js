import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "react-router-dom";
import "./CourseModule.css";


export function CourseModule({ module }) {
    return (
        <Link
            className="module-link"
            key={module.moduleName}
            to={"/resource-center/" + module.moduleName}
            // Allows module name & posts to be accessed in component that renders post
            // This allows us to filter the posts depending on the module name
            state={{ moduleName: module.moduleName }}>
            <div className="module-grid-item">
                <div>
                    <FontAwesomeIcon icon={module.icon} className="module-icon" />
                </div>
                <h2>{module.moduleName}</h2>
            </div>
        </Link>
    );
}