import { Link } from "react-router-dom";

import "./ScreenTooSmall.css"

export function ScreenTooSmall() {
    return (
        <div className="screen-too-small">
            <h1>Screen Too Small</h1>
            {/* Let user know this featur is only available on desktop/laptop and apologies */}
            <p>Unfortunately, this feature is only available on desktop/laptop. Apologies for the inconvenience.</p>
            <Link className="back-modules-link" to="/resource-center" replace>Back to Modules</Link>
        </div>
    )
}