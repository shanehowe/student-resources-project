import { useState, forwardRef, useImperativeHandle } from "react";
import AnimateHeight from 'react-animate-height';
import Proptypes from 'prop-types';

import "./Togglable.css";

export const Togglable = forwardRef((props, refs) => {
    const [visible, setVisible] = useState(false);
    const [formHeight, setFormHeight] = useState(0);

    const toggleVisibility = () => {
        setVisible(!visible);
        setFormHeight(formHeight === 0 ? 'auto' : 0);
    }

    useImperativeHandle(refs, () => {
        return {
            toggleVisibility
        }
    });

    return (
        <div className="toggle-container">
            <div className="button-container">
                {!visible && <button className="toggle-button" onClick={toggleVisibility}>{props.buttonLabel}</button>}
            </div>
            <AnimateHeight height={formHeight} duration={500}>
                {props.children}
                <div className="button-container">
                    <button   className="toggle-button" onClick={toggleVisibility} >Cancel</button>
                </div>
            </AnimateHeight>
        </div>
    )
});

Togglable.propTypes = {
    buttonLabel: Proptypes.string.isRequired
}