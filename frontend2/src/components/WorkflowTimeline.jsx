import { FiCheckCircle, FiClock, FiLoader } from "react-icons/fi";

function WorkflowTimeline({ currentStep, completed }) {
  const steps = [
    "Generate Timesheets"
  ];

  return (
    <div className="timeline-card">
      <h3>Workflow Timeline</h3>

      {steps.map((step, index) => (
        <div key={index} className="timeline-item">
          <div className="timeline-icon">
            {completed[index] ? (
              <FiCheckCircle className="done" />
            ) : currentStep === index ? (
              <FiLoader className="running spin" />
            ) : (
              <FiClock />
            )}
          </div>

          <div>
            <h4>{step}</h4>

            <p>
              {completed[index]
                ? "Completed"
                : currentStep === index
                ? "Running..."
                : "Waiting"}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default WorkflowTimeline;