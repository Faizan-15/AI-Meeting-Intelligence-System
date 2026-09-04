import { useRef, useState } from "react";
import "./MeetingInsights.css";

import Overview from "../Overview";
import MeetingPlayer from "../MeetingPlayer";
import Transcript from "../Transcript";
import AskAI from "../AskAI";

import InsightCard from "../InsightCard/InsightCard";
import ActionItems from "../ActionItems/ActionItems";
import Deadlines from "../Deadlines/Deadlines";
import UnresolvedIssues from "../UnresolvedIssues/UnresolvedIssues";
import FollowUpItems from "../FollowUpItems/FollowUpItems";

function MeetingInsights() {
  const [activeNav, setActiveNav] = useState("Meetings");

  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfile, setShowProfile] = useState(false);

  const playerRef = useRef(null);

  const handleNavigation = (item) => {
    setActiveNav(item);

    if (item === "Meetings") {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    } else {
      alert(`${item} page will be connected later.`);
    }
  };

  const handleBackToMeetings = () => {
    setActiveNav("Meetings");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const handleTimestampClick = (seconds) => {
    if (playerRef.current) {
      playerRef.current.jumpToTime(seconds);
    }

    const player = document.querySelector(".meeting-player-section");

    if (player) {
      player.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    }
  };

  const toggleNotifications = () => {
    setShowNotifications(!showNotifications);
    setShowProfile(false);
  };

  const toggleProfile = () => {
    setShowProfile(!showProfile);
    setShowNotifications(false);
  };

  return (
    <div className="app">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="logo">✦ MeetAI</div>

        <nav>
          <div
            className={`nav-item ${activeNav === "Dashboard" ? "active" : ""}`}
            onClick={() => handleNavigation("Dashboard")}
          >
            ⌂ Dashboard
          </div>

          <div
            className={`nav-item ${activeNav === "Meetings" ? "active" : ""}`}
            onClick={() => handleNavigation("Meetings")}
          >
            ▣ Meetings
          </div>

          <div
            className={`nav-item ${activeNav === "Calendar" ? "active" : ""}`}
            onClick={() => handleNavigation("Calendar")}
          >
            ◷ Calendar
          </div>
        </nav>

        <div className="sidebar-bottom">
          <div
            className={`nav-item ${activeNav === "Settings" ? "active" : ""}`}
            onClick={() => handleNavigation("Settings")}
          >
            ⚙ Settings
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">
        {/* TOPBAR */}
        <header className="topbar">
          <span className="breadcrumb">
            Meetings / Product Strategy Meeting
          </span>

          <div className="profile">
            {/* NOTIFICATION */}
            <div className="topbar-dropdown-wrapper">
              <button
                className="notification-button"
                onClick={toggleNotifications}
                aria-label="Notifications"
              >
                🔔
                <span className="notification-dot"></span>
              </button>

              {showNotifications && (
                <div className="topbar-dropdown notification-dropdown">
                  <div className="dropdown-header">
                    <strong>Notifications</strong>
                    <span>1 new</span>
                  </div>

                  <div className="notification-item">
                    <div className="notification-icon">✓</div>

                    <div>
                      <strong>Meeting insights ready</strong>
                      <p>
                        AI analysis for Product Strategy Meeting is available.
                      </p>
                      <small>Just now</small>
                    </div>
                  </div>

                  <div className="notification-footer">
                    View all notifications
                  </div>
                </div>
              )}
            </div>

            {/* PROFILE */}
            <div className="topbar-dropdown-wrapper">
              <button
                className="profile-button"
                onClick={toggleProfile}
                aria-label="Profile"
              >
                <div className="avatar">M</div>
              </button>

              {showProfile && (
                <div className="topbar-dropdown profile-dropdown">
                  <div className="profile-dropdown-header">
                    <div className="large-avatar">M</div>

                    <div>
                      <strong>Mina</strong>
                      <span>Frontend Developer</span>
                    </div>
                  </div>

                  <div className="profile-menu-item">👤 My Profile</div>

                  <div className="profile-menu-item">⚙ Settings</div>

                  <div className="profile-menu-divider"></div>

                  <div className="profile-menu-item logout">↪ Log out</div>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* MEETING HEADER */}
        <section className="meeting-header">
          <div>
            <button className="back-button" onClick={handleBackToMeetings}>
              ← Back to Meetings
            </button>

            <h1>Product Strategy Meeting</h1>

            <p className="meeting-meta">
              September 2, 2026
              <span>•</span>
              45 minutes
              <span>•</span>6 participants
            </p>
          </div>

          <span className="status">✓ Completed</span>
        </section>

        {/* OVERVIEW */}
        <Overview />

        {/* MEETING PLAYER */}
        <MeetingPlayer ref={playerRef} />

        {/* TRANSCRIPT */}
        <Transcript onTimestampClick={handleTimestampClick} />

        {/* AI INSIGHTS */}
        <section className="insights-section">
          <div className="section-heading">
            <div>
              <h2>✦ AI Insights</h2>

              <p>
                Important information automatically extracted from this meeting
              </p>
            </div>

            <span className="ai-badge">✦ AI Generated</span>
          </div>

          <div className="insights-grid">
            <InsightCard
              title="Key Discussion Points"
              subtitle="3 important topics"
              icon="💡"
            >
              <div className="point">
                <span className="number">1</span>

                <p>
                  The team discussed the upcoming website launch and the
                  remaining development work.
                </p>
              </div>

              <div className="point">
                <span className="number">2</span>

                <p>
                  The homepage design needs to be finalized before the launch.
                </p>
              </div>

              <div className="point">
                <span className="number">3</span>

                <p>
                  The marketing campaign and launch promotion strategy were
                  reviewed.
                </p>
              </div>
            </InsightCard>

            <InsightCard title="Decisions" subtitle="2 decisions made" icon="✓">
              <div className="decision">
                <div>
                  <strong>Website launch date</strong>
                  <p>September 10, 2026</p>
                </div>

                <span className="decision-tag">Confirmed</span>
              </div>

              <div className="decision">
                <div>
                  <strong>Marketing campaign</strong>
                  <p>Campaign approved by the team</p>
                </div>

                <span className="decision-tag">Approved</span>
              </div>
            </InsightCard>
          </div>

          <ActionItems />

          <div className="insights-grid">
            <Deadlines />
            <UnresolvedIssues />
          </div>

          <FollowUpItems />
        </section>

        {/* ASK AI */}
        <AskAI onTimestampClick={handleTimestampClick} />
      </main>
    </div>
  );
}

export default MeetingInsights;
