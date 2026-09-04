function InsightCard({ title, subtitle, icon, children }) {
  return (
    <div className="insight-card">
      <div className="card-title">
        <span className="icon">{icon}</span>

        <div>
          <h3>{title}</h3>
          <small>{subtitle}</small>
        </div>
      </div>

      {children}
    </div>
  );
}

export default InsightCard;
