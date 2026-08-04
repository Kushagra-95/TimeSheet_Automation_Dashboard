function Console({ logs }) {

    return (

        <div className="console-card">

            <div className="console-header">

                <span className="red"></span>
                <span className="yellow"></span>
                <span className="green"></span>

                <h3>Execution Console</h3>

            </div>

            <pre>

                {logs || "Waiting for workflow..."}

            </pre>

        </div>

    );

}

export default Console;