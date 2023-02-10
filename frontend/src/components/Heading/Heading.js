import Proptypes from 'prop-types';
import "./Heading.css";

export function Heading({ message }) {
    return <h2>{message}</h2>;
}

Heading.propTypes = {
    message: Proptypes.string.isRequired
}