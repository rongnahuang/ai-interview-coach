import { useState } from 'react'

type QuestionSet = {
  technical: string[];
  behavioral: string[];
};

type EvaluationResult = {
  score: number;
  strengths: string[];
  weaknesses: string[];
  improved_answer: string;
  follow_up_question?: string;
};

type InterviewSummary = {
  overall_score: number;
  technical_score: number;
  communication_score: number;
  problem_solving_score: number;
  recommendation: string;
  summary: string;
};

function App() {
  const [resume, setResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [questions, setQuestions] = useState<QuestionSet>({ technical: [], behavioral: [] });
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [evaluations, setEvaluations] = useState<Record<string, EvaluationResult>>({});
  const [summary, setSummary] = useState<InterviewSummary | null>(null);

  const generateQuestions = async () => {
    const response = await fetch("http://localhost:8000/generate-questions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume, jobDescription })
    });

    const data = await response.json();
    setQuestions(data.questions as QuestionSet);
  };

  const handleAnswerChange = (question: string, value: string) => {
    setAnswers(prev => ({
      ...prev,
      [question]: value
    }));
  };

  const evaluateAnswer = async (question: string) => {
    const answer = answers[question];

    const response = await fetch("http://localhost:8000/evaluate-answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, answer })
    });

    const data = await response.json();

    setEvaluations(prev => ({
      ...prev,
      [question]: data
    }));
  };

  const finishInterview = async () => {
    const response = await fetch("http://localhost:8000/interview-summary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers })
    });

    const data = await response.json();
    setSummary(data);
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900 p-6">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <h1 className="text-3xl font-bold text-center mb-6">
          AI Interview Coach
        </h1>

        {/* Inputs */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <textarea
            className="p-3 border rounded-lg h-32"
            placeholder="Paste your resume..."
            value={resume}
            onChange={(e) => setResume(e.target.value)}
          />

          <textarea
            className="p-3 border rounded-lg h-32"
            placeholder="Paste job description..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
        </div>

        {/* Generate button */}
        <div className="text-center mb-8">
          <button
            onClick={generateQuestions}
            className="bg-black text-white px-6 py-2 rounded-lg hover:bg-gray-800"
          >
            Generate Interview Questions
          </button>
        </div>

        {/* Questions Section */}
        <div className="grid grid-cols-2 gap-6">

          {/* Technical */}
          <div>
            <h2 className="text-xl font-semibold mb-3">Technical Questions</h2>

            {questions.technical.map((question, idx) => (
              <div key={idx} className="bg-white p-4 rounded-xl shadow mb-4">

                <p className="font-medium mb-2">{question}</p>

                <textarea
                  className="w-full border rounded p-2 mb-2"
                  placeholder="Type your answer..."
                  onChange={(e) =>
                    handleAnswerChange(question, e.target.value)
                  }
                />

                <button
                  onClick={() => evaluateAnswer(question)}
                  className="bg-blue-500 text-white px-3 py-1 rounded"
                >
                  Evaluate
                </button>

                {evaluations[question] && (
                  <div className="mt-3 text-sm space-y-1">

                    <p className="font-bold">
                      Score: {evaluations[question].score}/10
                    </p>

                    <p className="text-green-600">
                      👍 {evaluations[question].strengths?.join(", ")}
                    </p>

                    <p className="text-red-500">
                      👎 {evaluations[question].weaknesses?.join(", ")}
                    </p>

                    <p className="text-gray-700">
                      💡 {evaluations[question].improved_answer}
                    </p>

                    {evaluations[question].follow_up_question && (
                      <p className="text-blue-600">
                        🔁 {evaluations[question].follow_up_question}
                      </p>
                    )}

                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Behavioral */}
          <div>
            <h2 className="text-xl font-semibold mb-3">Behavioral Questions</h2>

            {questions.behavioral.map((question, idx) => (
              <div key={idx} className="bg-white p-4 rounded-xl shadow mb-4">

                <p className="font-medium mb-2">{question}</p>

                <textarea
                  className="w-full border rounded p-2 mb-2"
                  placeholder="Type your answer..."
                  onChange={(e) =>
                    handleAnswerChange(question, e.target.value)
                  }
                />

                <button
                  onClick={() => evaluateAnswer(question)}
                  className="bg-blue-500 text-white px-3 py-1 rounded"
                >
                  Evaluate
                </button>

                {evaluations[question] && (
                  <div className="mt-3 text-sm space-y-1">

                    <p className="font-bold">
                      Score: {evaluations[question].score}/10
                    </p>

                    <p className="text-green-600">
                      👍 {evaluations[question].strengths?.join(", ")}
                    </p>

                    <p className="text-red-500">
                      👎 {evaluations[question].weaknesses?.join(", ")}
                    </p>

                    <p className="text-gray-700">
                      💡 {evaluations[question].improved_answer}
                    </p>

                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Summary */}
        <div className="mt-10">
          <div className="text-center">
            <button
              onClick={finishInterview}
              className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
            >
              Finish Interview
            </button>
          </div>

          {summary && (
            <div className="mt-6 bg-white p-6 rounded-xl shadow space-y-2">

              <h2 className="text-xl font-bold mb-3">Interview Summary</h2>

              <p>Overall: {summary.overall_score}/10</p>
              <p>Technical: {summary.technical_score}/10</p>
              <p>Communication: {summary.communication_score}/10</p>
              <p>Problem Solving: {summary.problem_solving_score}/10</p>

              <h3 className="font-semibold mt-3">Recommendation</h3>
              <p>{summary.recommendation}</p>

              <h3 className="font-semibold mt-3">Summary</h3>
              <p>{summary.summary}</p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;