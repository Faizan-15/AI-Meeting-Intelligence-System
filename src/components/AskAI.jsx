import { useState } from "react";
import "./AskAI.css";

function AskAI({ onTimestampClick }) {
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      type: "ai",
      text: "Hi! I can answer questions about this meeting using its transcript and AI insights.",
    },
  ]);

  const suggestedQuestions = [
    "What was decided about the launch?",
    "Who is responsible for the homepage?",
    "What are the remaining tasks?",
  ];

  const getAnswer = (question) => {
    const lowerQuestion = question.toLowerCase();

    if (lowerQuestion.includes("launch") || lowerQuestion.includes("decided")) {
      return {
        text: "The team decided to launch the website on September 10, 2026.",
        timestamp: "00:21",
        seconds: 21,
      };
    }

    if (
      lowerQuestion.includes("homepage") ||
      lowerQuestion.includes("responsible")
    ) {
      return {
        text: "Ali is responsible for completing the homepage development.",
        timestamp: "00:21",
        seconds: 21,
      };
    }

    if (lowerQuestion.includes("task") || lowerQuestion.includes("remaining")) {
      return {
        text: "The remaining tasks include completing the homepage, preparing the marketing campaign, and preparing the launch announcement.",
        timestamp: "00:29",
        seconds: 29,
      };
    }

    return {
      text: "Based on this meeting, the team discussed the website launch, homepage development, marketing campaign, and remaining responsibilities.",
      timestamp: "00:02",
      seconds: 2,
    };
  };

  const sendMessage = () => {
    if (!question.trim() || isLoading) return;

    const userQuestion = question.trim();

    setMessages((previous) => [
      ...previous,
      {
        type: "user",
        text: userQuestion,
      },
    ]);

    setQuestion("");
    setIsLoading(true);

    const answer = getAnswer(userQuestion);

    setTimeout(() => {
      setMessages((previous) => [
        ...previous,
        {
          type: "ai",
          text: answer.text,
          timestamp: answer.timestamp,
          seconds: answer.seconds,
        },
      ]);

      setIsLoading(false);
    }, 1000);
  };

  const handleSuggestedQuestion = (item) => {
    if (isLoading) return;

    setQuestion(item);
  };

  const handleTimestampClick = (seconds) => {
    if (onTimestampClick) {
      onTimestampClick(seconds);
    }
  };

  return (
    <section className="ask-ai-section">
      <div className="ask-ai-header">
        <div>
          <h2>✦ Ask AI</h2>

          <p>Ask questions about this meeting</p>
        </div>

        <span className="context-badge">Meeting Context</span>
      </div>

      <div className="chat-box">
        <div className="messages">
          {messages.map((message, index) => (
            <div className={`message-row ${message.type}`} key={index}>
              {message.type === "ai" && <div className="ai-avatar">✦</div>}

              <div className="message-content">
                <div className="message-bubble">{message.text}</div>

                {message.timestamp && (
                  <button
                    className="chat-timestamp"
                    onClick={() => handleTimestampClick(message.seconds)}
                  >
                    ▶ {message.timestamp}
                  </button>
                )}
              </div>
            </div>
          ))}

          {/* LOADING MESSAGE */}
          {isLoading && (
            <div className="message-row ai">
              <div className="ai-avatar">✦</div>

              <div className="message-content">
                <div className="message-bubble ai-loading">
                  <span>AI is thinking</span>

                  <span className="loading-dots">
                    <span>.</span>
                    <span>.</span>
                    <span>.</span>
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* SUGGESTIONS */}
        <div className="suggestions">
          <span>Try asking:</span>

          <div className="suggestion-buttons">
            {suggestedQuestions.map((item, index) => (
              <button
                key={index}
                onClick={() => handleSuggestedQuestion(item)}
                disabled={isLoading}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        {/* INPUT */}
        <div className="chat-input-area">
          <input
            type="text"
            placeholder="Ask something about this meeting..."
            value={question}
            disabled={isLoading}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
          />

          <button
            className="send-button"
            onClick={sendMessage}
            disabled={isLoading}
          >
            {isLoading ? "..." : "➤"}
          </button>
        </div>
      </div>
    </section>
  );
}

export default AskAI;
