function ActionItems() {
  const actions = [
    {
      task: "Finish homepage development",
      owner: "Ali",
      deadline: "Sep 5",
      status: "Pending",
    },
    {
      task: "Prepare marketing campaign",
      owner: "Sara",
      deadline: "Sep 7",
      status: "Pending",
    },
    {
      task: "Prepare launch announcement",
      owner: "Mina",
      deadline: "Sep 8",
      status: "In Progress",
    },
  ];

  return (
    <div className="insight-card action-card">
      <div className="card-title">
        <span className="icon">✓</span>

        <div>
          <h3>Action Items</h3>
          <small>Tasks assigned during the meeting</small>
        </div>
      </div>

      <div className="action-table">
        <div className="action-header">
          <span>Task</span>
          <span>Owner</span>
          <span>Deadline</span>
          <span>Status</span>
        </div>

        {actions.map((action, index) => (
          <div className="action-row" key={index}>
            <span className="task-name">{action.task}</span>

            <span className="owner">
              <span className="mini-avatar">{action.owner.charAt(0)}</span>

              {action.owner}
            </span>

            <span>{action.deadline}</span>

            <span
              className={
                action.status === "Pending" ? "pending" : "in-progress"
              }
            >
              {action.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ActionItems;
