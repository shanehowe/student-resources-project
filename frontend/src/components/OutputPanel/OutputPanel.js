import "./OutputPanel.css";

export function OutputPanel({ output }) {

    return (
        <div className="output-panel">
            <div>
                <pre className="std-out">{output}</pre>
            </div>
        </div>
    )
}