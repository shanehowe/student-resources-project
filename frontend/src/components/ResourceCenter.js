import { Navigation } from "./Navigation/Navigation";
import { CourseModules } from "./CourseModules/CourseModules";
import { Heading } from "./Heading/Heading";
import { useAuth } from "./AuthProvider";


export function ResourceCenter() {
    const auth = useAuth();

    return (
        <>
            <Navigation />
            <Heading message={"It's nice to see you, " + auth.user.username} />
            <CourseModules />
        </>
    );
}