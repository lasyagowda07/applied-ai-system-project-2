type ConflictWarningsProps = {
    warnings: string[];
    conflicts: unknown[];
  };
  
  export default function ConflictWarnings({
    warnings,
    conflicts,
  }: ConflictWarningsProps) {
    return (
      <div className="card">
        <h2>Warnings and Conflicts</h2>
  
        {(!warnings || warnings.length === 0) &&
        (!conflicts || conflicts.length === 0) ? (
          <p className="success">No major warnings found.</p>
        ) : (
          <>
            {warnings.map((warning, index) => (
              <div className="warning" key={`${warning}-${index}`}>
                {warning}
              </div>
            ))}
  
            {conflicts.length > 0 && (
              <p className="small-muted">
                Conflict detector found {conflicts.length} possible conflict(s).
              </p>
            )}
          </>
        )}
      </div>
    );
  }