import Proptypes from 'prop-types';

export function Notification({ message, isError }) {
    if (message === null) {
        return null;
    }
    const style = {
        color: isError === true ? 'red' : 'green',
        background: 'lightgrey',
        fontSize: 20,
        borderStyle: 'solid',
        borderRadius: 5,
        padding: 10,
        marginBottom: 10,
        textAlign: "center"
    };
    return (
        <div style={style}>
            <p>{message}</p>
        </div>
    );
}

Notification.propTypes = {
    message: Proptypes.string,
    isError: Proptypes.bool.isRequired
}