function ProgressSection({ progress }) {

    return (

        <div className="progress-card">

            <div className="progress-header">

                <h3>Workflow Progress</h3>

                <span>{progress}%</span>

            </div>

            <div className="progress">

                <div
                    className="progress-fill"
                    style={{ width: `${progress}%` }}
                />

            </div>

        </div>

    );

}

export default ProgressSection;