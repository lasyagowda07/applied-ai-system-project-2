type Pet = {
    name: string;
    species: string;
    age?: number | null;
  };
  
  type ExtractedDataCardProps = {
    pets: Pet[];
  };
  
  export default function ExtractedDataCard({ pets }: ExtractedDataCardProps) {
    return (
      <div className="card">
        <h2>Extracted Pets</h2>
  
        {!pets || pets.length === 0 ? (
          <p className="small-muted">No pets extracted yet.</p>
        ) : (
          pets.map((pet) => (
            <div key={pet.name} className="success">
              <strong>{pet.name}</strong>
              <div>Species: {pet.species || "unknown"}</div>
              <div>Age: {pet.age ?? "not provided"}</div>
            </div>
          ))
        )}
      </div>
    );
  }