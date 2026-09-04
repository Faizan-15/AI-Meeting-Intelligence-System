import { useState } from "react";
import "./Transcript.css";

function Transcript({ onTimestampClick }) {
  const [search, setSearch] = useState("");

  const transcript = [
    {
      time: "00:02",
      seconds: 2,
      speaker: "Ali",
      text: "Let's discuss the website launch timeline first.",
    },
    {
      time: "00:08",
      seconds: 8,
      speaker: "Sara",
      text: "I think we can launch by September 10 if the remaining work is completed.",
    },
    {
      time: "00:15",
      seconds: 15,
      speaker: "Mina",
      text: "What about the homepage design? Is it ready for development?",
    },
    {
      time: "00:21",
      seconds: 21,
      speaker: "Ali",
      text: "The homepage should be completed before the final launch.",
    },
    {
      time: "00:29",
      seconds: 29,
      speaker: "Sara",
      text: "We also need to prepare the marketing campaign before launch.",
    },
    {
      time: "00:36",
      seconds: 36,
      speaker: "Mina",
      text: "Okay, I will prepare the launch announcement content.",
    },
    {
      time: "00:42",
      seconds: 42,
      speaker: "Ali",
      text: "Great. Let's finalize the remaining tasks and deadlines.",
    },
  ];

  const filteredTranscript = transcript.filter((item) =>
    `${item.speaker} ${item.text}`.toLowerCase().includes(search.toLowerCase()),
  );

  const handleTimestampClick = (seconds) => {
    if (onTimestampClick) {
      onTimestampClick(seconds);
    }
  };

  return (
    <section className="transcript-section">
      <div className="transcript-header">
        <div>
          <h2>Transcript</h2>

          <p>Search and review the meeting conversation</p>
        </div>

        <span className="transcript-count">{transcript.length} entries</span>
      </div>

      <div className="transcript-search">
        <span>⌕</span>

        <input
          type="text"
          placeholder="Search transcript..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        {search && <button onClick={() => setSearch("")}>×</button>}
      </div>

      <div className="transcript-list">
        {filteredTranscript.length > 0 ? (
          filteredTranscript.map((item, index) => (
            <div className="transcript-row" key={index}>
              <button
                className="timestamp"
                onClick={() => handleTimestampClick(item.seconds)}
              >
                ▶ {item.time}
              </button>

              <div className="speaker-avatar">{item.speaker.charAt(0)}</div>

              <div className="transcript-content">
                <strong>{item.speaker}</strong>

                <p>{item.text}</p>
              </div>
            </div>
          ))
        ) : (
          <div className="no-results">No transcript found.</div>
        )}
      </div>
    </section>
  );
}

export default Transcript;
