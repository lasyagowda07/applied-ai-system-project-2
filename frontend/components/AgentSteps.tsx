type AgentStepsProps = {
    steps: string[];
  };
  
  export default function AgentSteps({ steps }: AgentStepsProps) {
    return (
      <div className="card">
        <h2>Agentic Workflow</h2>
  
        {!steps || steps.length === 0 ? (
          <p className="small-muted">No agent steps yet.</p>
        ) : (
          <ol className="agent-list">
            {steps.map((step, index) => (
              <li key={`${step}-${index}`}>{step}</li>
            ))}
          </ol>
        )}
      </div>
    );
  }