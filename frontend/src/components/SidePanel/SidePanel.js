import "./SidePanel.css";

export function SidePanel({ challenge }) {
    return (
        <div className='side-panel-container'>
            <div>
                <h2>{challenge.name}</h2>
            </div>

            <div>
                <p id="prompt">{challenge.prompt}</p><br/>
                
            </div>

            <div>
                <p>Examples:</p>
                <Examples examples={challenge.examples} />
            </div>
            
            {challenge.assumptions &&
            <div> 
                <h4>Assumptions:</h4>
                {challenge.assumptions.map((assumption) => {
                        return <div key={assumption}><p>•{assumption}</p></div>
                    })}
            </div>}
            
                    
        </div>
    )
}


function Examples({ examples }) {
    return examples.map((e) => <div key={e.exampleInput} className="examples-container">
        <span className="examples">Input:</span> <pre>{e.exampleInput}</pre>
        <span className="examples">Output:</span> <pre>{e.exampleOutput}</pre>
    </div>)
}