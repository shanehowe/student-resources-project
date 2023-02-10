import { Challenge } from "../Challenge/Challenge";
import Proptypes from 'prop-types';

import "./ChallengeList.css";

export function ChallengeList({ challenges, handleSettingChallenge }) {
    return challenges.map((challenge) => {
        return <div key={challenge._id} className="challenge__">
                <Challenge 
                    challenge={challenge} 
                    handleSettingChallenge={handleSettingChallenge} />
               </div>
    })
}

ChallengeList.propTypes = {
    challenges: Proptypes.arrayOf(Object).isRequired,
    handleSettingChallenge: Proptypes.func.isRequired
}