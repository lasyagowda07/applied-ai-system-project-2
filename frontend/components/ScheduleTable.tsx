type ScheduleItem = {
    pet_name: string;
    description: string;
    task_type: string;
    time: string | null;
    recurrence: string | null;
    priority: number;
    completed: boolean;
  };
  
  type ScheduleTableProps = {
    schedule: ScheduleItem[];
  };
  
  export default function ScheduleTable({ schedule }: ScheduleTableProps) {
    if (!schedule || schedule.length === 0) {
      return (
        <div className="card">
          <h2>Generated Schedule</h2>
          <p className="small-muted">No schedule generated yet.</p>
        </div>
      );
    }
  
    return (
      <div className="card">
        <h2>Generated Schedule</h2>
  
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Pet</th>
                <th>Task</th>
                <th>Type</th>
                <th>Time</th>
                <th>Recurrence</th>
                <th>Priority</th>
                <th>Status</th>
              </tr>
            </thead>
  
            <tbody>
              {schedule.map((task, index) => (
                <tr key={`${task.pet_name}-${task.time}-${index}`}>
                  <td>{task.pet_name}</td>
                  <td>{task.description}</td>
                  <td>
                    <span className="pill">{task.task_type}</span>
                  </td>
                  <td>{task.time || "Missing"}</td>
                  <td>{task.recurrence || "None"}</td>
                  <td>{task.priority}</td>
                  <td>{task.completed ? "Complete" : "Pending"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }