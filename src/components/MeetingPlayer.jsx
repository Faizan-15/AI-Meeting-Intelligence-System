import { forwardRef, useImperativeHandle, useRef, useState } from "react";

import "./MeetingPlayer.css";

const MeetingPlayer = forwardRef(function MeetingPlayer(props, ref) {
  const audioRef = useRef(null);

  const [currentTime, setCurrentTime] = useState(0);

  useImperativeHandle(ref, () => ({
    jumpToTime(seconds) {
      if (audioRef.current) {
        audioRef.current.currentTime = seconds;
        setCurrentTime(seconds);

        audioRef.current.play().catch(() => {
          // Browser may block automatic playback
        });
      }
    },
  }));

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);

    return `${String(minutes).padStart(2, "0")}:${String(
      remainingSeconds,
    ).padStart(2, "0")}`;
  };

  return (
    <section className="meeting-player-section">
      <div className="player-header">
        <div>
          <h2>Meeting Recording</h2>

          <p>Listen to the meeting and jump to important timestamps</p>
        </div>

        <span className="recording-badge">● Recording</span>
      </div>

      <div className="player-card">
        <div className="player-info">
          <div className="recording-icon">▶</div>

          <div>
            <strong>Product Strategy Meeting</strong>

            <span>September 2, 2026 • 45 minutes</span>
          </div>
        </div>

        <audio
          ref={audioRef}
          controls
          onTimeUpdate={(e) => setCurrentTime(e.target.currentTime)}
        >
          {/* Actual meeting recording URL will be added here later */}
        </audio>

        <div className="player-time">
          Current position: <strong>{formatTime(currentTime)}</strong>
        </div>
      </div>
    </section>
  );
});

export default MeetingPlayer;
