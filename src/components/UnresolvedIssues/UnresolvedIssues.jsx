import InsightCard from "../InsightCard/InsightCard";

function UnresolvedIssues() {
  const issues = [
    {
      title: "Marketing budget",
      description: "Final budget approval is still pending.",
    },
    {
      title: "Launch announcement",
      description: "Final announcement content has not been approved.",
    },
    {
      title: "Analytics tracking",
      description: "Tracking requirements still need confirmation.",
    },
  ];

  return (
    <InsightCard
      title="Unresolved Issues"
      subtitle="Items requiring follow-up"
      icon="⚠"
    >
      {issues.map((issue, index) => (
        <div className="issue" key={index}>
          <span>!</span>

          <div>
            <strong>{issue.title}</strong>

            <p>{issue.description}</p>
          </div>
        </div>
      ))}
    </InsightCard>
  );
}

export default UnresolvedIssues;
