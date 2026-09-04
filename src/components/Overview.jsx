import { useState } from "react";
import "./Overview.css";
function Overview() {
  const [summaryType, setSummaryType] = useState("short");

  const summaries = {
    short:
      "Team finalized the website launch for September 10, 2026 and assigned remaining homepage and marketing tasks.",
    detailed:
      "The team discussed the upcoming website launch, homepage development, marketing strategy, and remaining tasks. The team agreed on September 10, 2026 as the final launch date and assigned responsibilities for the remaining work.",
  };

  const participants = [
    { name: "Ali", role: "Product Manager" },
    { name: "Sara", role: "Marketing Lead" },
    { name: "Mina", role: "UI/UX Designer" },
    { name: "Huzaifa", role: "Developer" },
    { name: "Shehryar", role: "Developer" },
    { name: "Subhan", role: "Marketing" },
  ];

  return (
    <section className="overview-section">
      {/* SECTION HEADER */}

      <div className="overview-heading">
        <div>
          <h2>Overview</h2>
          <p>Summary and important meeting information</p>
        </div>

        <span className="sentiment">● Positive</span>
      </div>

      {/* SUMMARY */}

      <div className="overview-summary">
        <div className="summary-icon">✦</div>

        <div>
          <div className="summary-title-row">
            <h3>Meeting Summary</h3>

            <div className="summary-toggle">
              <button
                className={summaryType === "short" ? "active" : ""}
                onClick={() => setSummaryType("short")}
              >
                Short
              </button>

              <button
                className={summaryType === "detailed" ? "active" : ""}
                onClick={() => setSummaryType("detailed")}
              >
                Detailed
              </button>
            </div>
          </div>

          <p>{summaries[summaryType]}</p>
        </div>
      </div>

      {/* INFO CARDS */}

      <div className="overview-info-grid">
        <div className="overview-info-card">
          <span className="info-icon">📅</span>

          <div>
            <small>Date</small>
            <strong>September 2, 2026</strong>
          </div>
        </div>

        <div className="overview-info-card">
          <span className="info-icon">⏱</span>

          <div>
            <small>Duration</small>
            <strong>45 minutes</strong>
          </div>
        </div>

        <div className="overview-info-card">
          <span className="info-icon">👥</span>

          <div>
            <small>Participants</small>
            <strong>6 people</strong>
          </div>
        </div>

        <div className="overview-info-card">
          <span className="info-icon">✓</span>

          <div>
            <small>Status</small>
            <strong>Completed</strong>
          </div>
        </div>
      </div>

      {/* PARTICIPANTS */}

      <div className="participants-card">
        <div className="participants-header">
          <div>
            <h3>Participants</h3>
            <p>People who attended this meeting</p>
          </div>

          <span>{participants.length} participants</span>
        </div>

        <div className="participants-list">
          {participants.map((person, index) => (
            <div className="participant" key={index}>
              <div className="participant-avatar">{person.name.charAt(0)}</div>

              <div>
                <strong>{person.name}</strong>
                <small>{person.role}</small>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default Overview;
