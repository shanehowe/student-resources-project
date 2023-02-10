import Editor from "@monaco-editor/react";

import "./MonacoTextEditor.css"

export function MonacoTextEditor({ 
    boilerPlateCode, handleEditorDidMount, handleCodeSubmission
}) {
    

    return (
        <div className="code-editor-container">
            <div className="run-submit-btns">
                <button  onClick={handleCodeSubmission} >Submit</button>
            </div>

            <Editor 
                height="40vh"
                defaultValue={boilerPlateCode}
                defaultLanguage="python"
                onMount={handleEditorDidMount}
                options={{ "fontSize": "14rem" }}
                theme="vs"
            />
        </div>
    )
}