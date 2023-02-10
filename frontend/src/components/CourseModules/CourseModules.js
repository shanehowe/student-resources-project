import "./CourseModules.css";
import { faDatabase, faFileCode, faPlusMinus } from "@fortawesome/free-solid-svg-icons";
import { faPython, faLinux } from "@fortawesome/free-brands-svg-icons";
import { CourseModule } from "../CourseModule/CourseModule";

export function CourseModules() {
    const modules = [
        {
            moduleName: "Structured Programming 2",
            icon: faPython
        },
        {
            moduleName: "Database Concepts",
            icon: faDatabase
        },
        {
            moduleName: "Mathematics",
            icon: faPlusMinus
        },
        {
            moduleName: "Operating Systems 1",
            icon: faLinux
        },
        {
            moduleName: "Web Development 2",
            icon: faFileCode
        }
    ];

    return (
        <div className="module-grid">
            {modules.map((module) => {
                return <CourseModule key={module.moduleName} module={module} />;
            })}
        </div>
    );

}