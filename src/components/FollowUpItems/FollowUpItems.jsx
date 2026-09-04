import InsightCard from "../InsightCard/InsightCard";

function FollowUpItems() {
  const followUps = [
    {
      title: "Share homepage preview",
      description: "Ali will circulate the updated homepage preview once ready.",
    },
    {
      title: "Confirm marketing assets",
      description: "Sara to confirm final marketing assets with the design team.",
    },
    {
      title: "Schedule pre-launch check-in",
      description: "Team to schedule a short check-in before September 10.",
    },
  ];

  return (
    <InsightCard
      title="Follow-up Items"
      subtitle="Things to revisit next"
      icon="↻"
    >
      {followUps.map((item, index) => (
        <div className="issue" key={index}>
          <span>→</span>

          <div>
            <strong>{item.title}</strong>

            <p>{item.description}</p>
          </div>
        </div>
      ))}
    </InsightCard>
  );
}

export default FollowUpItems;
