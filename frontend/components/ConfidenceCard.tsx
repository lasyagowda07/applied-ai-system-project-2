type ConfidenceCardProps = {
    confidence: number | null;
  };
  
  function getLabel(confidence: number) {
    if (confidence >= 0.8) return "High confidence";
    if (confidence >= 0.6) return "Medium confidence";
    return "Low confidence";
  }
  
  export default function ConfidenceCard({ confidence }: ConfidenceCardProps) {
    return (
      <div className="card">
        <h2>Confidence Score</h2>
  
        {confidence === null ? (
          <p className="small-muted">No confidence score yet.</p>
        ) : (
          <>
            <div className="confidence-number">{Math.round(confidence * 100)}%</div>
            <p className="small-muted">{getLabel(confidence)}</p>
          </>
        )}
      </div>
    );
  }