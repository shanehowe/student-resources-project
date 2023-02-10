import Proptypes from 'prop-types';

import "./Challenge.css";

export function Challenge({ challenge, handleSettingChallenge }) {
    return (
        <div className="challenge" >
                <p className="title">{challenge.name}</p>
                <button className="btn" onClick={() => handleSettingChallenge(challenge)}>Try</button>
        </div>
    )
}

Challenge.propTypes = {
    challenge: Proptypes.object.isRequired,
    handleSettingChallenge: Proptypes.func.isRequired
}