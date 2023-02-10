import { useEffect, useRef, useState } from "react";
import { Navigation } from "../Navigation/Navigation";
import { ChallengeList } from "../ChallengeList/ChallengeList";
import { MonacoTextEditor } from "../MonacoTextEditor/MonacoTextEditor";
import { SidePanel } from "../SidePanel/SidePanel";
import { OutputPanel } from "../OutputPanel/OutputPanel";
import { ScreenTooSmall } from "../ScreenTooSmall/ScreenTooSmall";
import ReactConfetti from "react-confetti";
import codeServices from "../../services/codeSubmission";
import useWindowSize from "../windowSize";
import { useNavigate } from "react-router-dom";

import "./PythonChallenges.css";

export const PythonChallenges = ({ handleLogout, challenges, challenge, handleSettingChallenge, notify }) => {
    const [output, setOutput] = useState("Your output will be displayed here");
    const [codePassedTests, setCodePassedTests] = useState(false);
    const [stringChallenges, setStringChallenges] = useState([]);
    const [listChallanges, setListChallenges] = useState([]);
    const [arithmeticChallenges, setArithmeticChallenges] = useState([]);
    const navigate = useNavigate();

    const editorRef = useRef(null);

    const { width, height } = useWindowSize();

    useEffect(() => {
        setOutput("Your output will be displayed here")
    }, [challenge]);

    useEffect(() => {
        const lists = challenges.filter(c => c.category === "lists");
        const inputValidation = challenges.filter(c => c.category === "arithmetic");
        const strings = challenges.filter(c => c.category === "strings");

        setListChallenges(lists);
        setArithmeticChallenges(inputValidation);
        setStringChallenges(strings);
    }, [challenges]);

    const handleEditorDidMount = (editor, monaco) => {
        editorRef.current = editor;
    }
    
    const handleCodeSubmission = async () => {
        setOutput("Running Test Cases.. Hang Tight!")
        try {
            const response = await codeServices.submitCode(editorRef.current.getValue(), challenge.functionName);
            if (response.data.status.id === 5) {
                setOutput("Maximum Time Limit exceeded.\nYou likely have an infinite loop.")
            } else if (response.data.stdout === "True\n") {
                setOutput("Your code passed all test cases!!\n🥳🥳🥳🥳🥳🥳🥳🥳🥳")
                setCodePassedTests(true);
                setTimeout(() => {
                    setCodePassedTests(false);
                }, 10000);
            } else if (response.data.stderr) {
                setOutput(response.data.stderr);
            } else {
                setOutput(response.data.stdout);
            }
        } catch (error) {
            if (error.response.data.detail === "token has expired") {
                notify("Your session has expired. Log back in to continue", true);
                navigate("/login", {replace: true});
            }
            if (error.response.data.detail === "No print statement allowed in source code.") {
                setOutput("Remove all print statements before submitting source code");
            } else {
                setOutput("An unexpected error occured.");    
            }    
        }
    }

    if (width < 700) {
        return (
            <>
            <Navigation handleLogout={handleLogout}/>
            <ScreenTooSmall />
            </>
        )
    }

    return (
        <>
        <Navigation handleLogout={handleLogout}/>
        {codePassedTests === true && <ReactConfetti width={width} height={height} gravity={0.8}  />}
        {challenge == null ?
        <div className="content-wrapper">
         <div className="category">
            <h3>Strings</h3>
            <ChallengeList challenges={stringChallenges} handleSettingChallenge={handleSettingChallenge} />
         </div>

         <div className="category">
            <h3>Lists</h3>
            <ChallengeList challenges={listChallanges} handleSettingChallenge={handleSettingChallenge} />
         </div>

         <div className="category">
            <h3>Arithmetic</h3>
            <ChallengeList challenges={arithmeticChallenges} handleSettingChallenge={handleSettingChallenge} />
         </div>
        </div>
        :
        <div className="coding-challenge-container">
            <div>
                <button id="back-btn" onClick={() => handleSettingChallenge(null)}>Back to challenges</button>
            </div>
            
            <MonacoTextEditor 
                boilerPlateCode={challenge.boilerPlateCode}
                handleEditorDidMount={handleEditorDidMount}
                handleCodeSubmission={handleCodeSubmission}
            />
            <OutputPanel 
                output={output} 
            />
            <SidePanel challenge={challenge}/>
            
        </div>
        }
        </>
    );
}