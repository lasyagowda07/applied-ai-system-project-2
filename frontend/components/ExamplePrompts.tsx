type ExamplePromptsProps = {
    setText: (value: string) => void;
  };
  
  const examples = [
    {
      label: "Simple schedule",
      text: "I have a dog named Bruno. Feed him at 8 AM and walk him at 6 PM.",
    },
    {
      label: "Conflict case",
      text: "I have a cat named Luna. Feed Luna at 8 AM and give medicine at 8 AM.",
    },
    {
      label: "Guardrail case",
      text: "My pet needs care tomorrow.",
    },
  ];
  
  export default function ExamplePrompts({ setText }: ExamplePromptsProps) {
    return (
      <div className="card">
        <h2>Example prompts</h2>
        <p className="small-muted">
          Use these to test normal scheduling, conflict detection, and guardrails.
        </p>
  
        <div className="example-row">
          {examples.map((example) => (
            <button
              key={example.label}
              className="example-button"
              onClick={() => setText(example.text)}
            >
              {example.label}
            </button>
          ))}
        </div>
      </div>
    );
  }