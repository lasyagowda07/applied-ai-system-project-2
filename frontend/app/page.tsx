"use client";

import { useState } from "react";

import InputBox from "../components/InputBox";
import ExamplePrompts from "../components/ExamplePrompts";
import ScheduleTable from "../components/ScheduleTable";
import ExtractedDataCard from "../components/ExtractedDataCard";
import ConfidenceCard from "../components/ConfidenceCard";
import ConflictWarnings from "../components/ConflictWarnings";
import AgentSteps from "../components/AgentSteps";
import ErrorMessage from "../components/ErrorMessage";

type ScheduleResponse = {
  owner: string;
  pets: {
    name: string;
    species: string;
    age?: number | null;
  }[];
  schedule: {
    pet_name: string;
    description: string;
    task_type: string;
    time: string | null;
    recurrence: string | null;
    priority: number;
    completed: boolean;
  }[];
  conflicts: unknown[];
  confidence: number;
  warnings: string[];
  agent_steps: string[];
};

const API_URL = "http://127.0.0.1:8000/api/schedule";

export default function HomePage() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<ScheduleResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error("Backend returned an error.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        "Could not connect to FastAPI backend. Make sure backend is running on http://127.0.0.1:8000."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <div className="container">
        <section className="hero">
          <h1>PawPal AI Planner</h1>
          <p className="subtitle">
            An AI-assisted pet care scheduler that converts natural language into
            structured tasks, builds a schedule, detects conflicts, and explains
            its decision process.
          </p>
        </section>

        <div className="grid">
          <InputBox
            text={text}
            setText={setText}
            onSubmit={handleSubmit}
            loading={loading}
          />

          <ExamplePrompts setText={setText} />

          <ErrorMessage message={error} />

          {result && (
            <>
              <ConfidenceCard confidence={result.confidence} />
              <ExtractedDataCard pets={result.pets} />
              <ScheduleTable schedule={result.schedule} />
              <ConflictWarnings
                warnings={result.warnings}
                conflicts={result.conflicts}
              />
              <AgentSteps steps={result.agent_steps} />
            </>
          )}
        </div>
      </div>
    </main>
  );
}