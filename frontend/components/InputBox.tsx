type InputBoxProps = {
    text: string;
    setText: (value: string) => void;
    onSubmit: () => void;
    loading: boolean;
  };
  
  export default function InputBox({
    text,
    setText,
    onSubmit,
    loading,
  }: InputBoxProps) {
    return (
      <div className="card">
        <h2>Describe your pet care routine</h2>
  
        <textarea
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="Example: I have a dog named Bruno. Feed him at 8 AM and walk him at 6 PM."
        />
  
        <button
          className="primary-button"
          onClick={onSubmit}
          disabled={loading || !text.trim()}
        >
          {loading ? "Planning..." : "Generate AI Schedule"}
        </button>
      </div>
    );
  }