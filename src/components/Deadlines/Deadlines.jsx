function Deadlines() {
  const deadlines = [
    {
      date: "05",
      month: "SEP",
      title: "Homepage completion",
      description: "Development must be completed",
    },
    {
      date: "07",
      month: "SEP",
      title: "Marketing campaign",
      description: "Campaign preparation deadline",
    },
    {
      date: "10",
      month: "SEP",
      title: "Website launch",
      description: "Final product launch date",
    },
  ];

  return (
    <div className="insight-card">
      <div className="card-title">
        <span className="icon">📅</span>

        <div>
          <h3>Deadlines</h3>
          <small>Important dates identified</small>
        </div>
      </div>

      {deadlines.map((deadline, index) => (
        <div className="deadline" key={index}>
          <div className="date-box">
            <strong>{deadline.date}</strong>
            <span>{deadline.month}</span>
          </div>

          <div>
            <strong>{deadline.title}</strong>
            <p>{deadline.description}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default Deadlines;
