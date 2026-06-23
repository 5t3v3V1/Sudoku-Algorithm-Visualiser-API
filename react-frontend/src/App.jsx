import Grid from './Grid'
import Board from './Board'
import { useState } from 'react';

function animate_steps(steps, setType, delay = 150) {
    let i = 0;
    const interval = setInterval (() => {
        if (i >= steps.length) {
            clearInterval(interval);
            return;
        };
        setType(steps[i])
        i ++;
    }, delay);
};

function App() {
    const [generatedBoard, setGeneratedBoard] = useState([]);
    const [boardStep, setBoardStep] = useState([])
    const [solvedBoard, setSolvedBoard] = useState([]);
    const [boardTime, setBoardTime] = useState(0);
    const [generatedGrid, setGeneratedGrid] = useState([]);
    const [solvedBfsGrid, setSolvedBfsGrid] = useState([]);
    const [bfsNodes, setBfsNodes] = useState(0);
    const [bfsTime, setBfsTime] = useState(0);
    const [solvedDfsGrid, setSolvedDfsGrid] = useState([]);
    const [dfsNodes, setDfsNodes] = useState(0);
    const [dfsTime, setDfsTime] = useState(0);
    const [solvedDijkstraGrid, setSolvedDijkstraGrid] = useState([]);
    const [dijkstraNodes, setDijkstraNodes] = useState(0);
    const [dijkstraTime, setDijkstraTime] = useState(0);
    const [solvedAstarGrid, setSolvedAstarGrid] = useState([]);
    const [astarNodes, setAstarNodes] = useState(0);
    const [astarTime, setAstarTime] = useState(0);
    const [bfsGridStep, setBfsGridStep] = useState([]);
    const [dfsGridStep, setDfsGridStep] = useState([]);
    const [dijkstraGridStep, setDijkstraGridStep] = useState([]);
    const [astarGridStep, setAstarGridStep] = useState([]);
    const [winner, setWinner] = useState("")

  
    async function generate_solved_board() {
      try {
        const response = await fetch("http://127.0.0.1:8000/generate_solve_board");
        if (!response.ok) throw new Error("Failed to generate board");
        const data = await response.json();

        console.log(data);
        setGeneratedBoard(data.generated_board);
        animate_steps(data.board_steps, setBoardStep)
        setSolvedBoard(data.solved_board);
        setBoardTime(data.time_ms.toFixed(2));
      } catch(err) {
        console.log(err);
      }
    };

    async function generate_solved_grid() {
      try {
        const response = await fetch("http://127.0.0.1:8000/generate_solve_grid");
        if (!response.ok) throw new Error("Failed to generate grid")
        const data = await response.json();

        console.log(data);
        setGeneratedGrid(data.generated_grid);
        setBfsNodes(data.bfs.bfs_nodes);
        setSolvedBfsGrid(data.bfs.solved_bfs_grid);
        animate_steps(data.bfs.bfs_steps, setBfsGridStep);
        setBfsTime(data.bfs.time_ms.toFixed(2));
        setDfsNodes(data.dfs.dfs_nodes);
        setSolvedDfsGrid(data.dfs.solved_dfs_grid);
        animate_steps(data.dfs.dfs_steps, setDfsGridStep);
        setDfsTime(data.dfs.time_ms.toFixed(2));
        setDijkstraNodes(data.dijkstra.dijkstra_nodes);
        setSolvedDijkstraGrid(data.dijkstra.solved_dijkstra_grid);
        animate_steps(data.dijkstra.dijkstra_steps, setDijkstraGridStep);
        setDijkstraTime(data.dijkstra.time_ms.toFixed(2));
        setAstarNodes(data.astar.astar_nodes);
        setSolvedAstarGrid(data.astar.solved_astar_grid);
        animate_steps(data.astar.astar_steps, setAstarGridStep);
        setAstarTime(data.astar.time_ms.toFixed(2));

        const results = [
            {name: "BFS", time: data.bfs.time_ms},
            {name: "DFS", time: data.dfs.time_ms},
            {name: "Dijkstra", time: data.dijkstra.time_ms},
            {name: "A*", time: data.astar.time_ms}
        ];

        results.sort((a,b) => a.time - b.time);

        setWinner(results[0].name)
      } catch(err) {
        console.log(err);
      };
    };

    return (
      <>
        <h1>Algorithm Visualiser</h1>
        <h2 style={{textAlign: 'center'}}>Description</h2>
        <p>Hi, this is algorithm visualiser which is able to solve and generate sudoku boards and 5x5 grids using BFS, DFS, Dijkstra and A* algorithms.</p>
        <p>Creator: 5t3v3V1</p>
        <h3>Options</h3>
        <button onClick={generate_solved_board}>Generate & Solve Board</button>
        <button onClick={generate_solved_grid}>Generate & Solve Grid</button>
        <div className='boards'>
          <div>
            <h4>Generated Board:</h4>
            <Board board={generatedBoard} />
          </div>
          <div>
            <h4>Steps:</h4>
            <Board board={boardStep} />
          </div>
          <div>
            <h4>Solved Board:</h4>
            <Board board={solvedBoard} />
          </div>
        </div>
        <div>Board Time: {boardTime}ms</div>
        <div className='generated'>
          <div>
            <h3>Generated Grid:</h3>
            <Grid grid={generatedGrid} />
          </div>
          <div>
            <h3>Node Classification</h3>
            <p className="cell wall" style={{width: '120px', textAlign: 'center', color: 'aliceblue'}}>Wall</p>
            <p className="cell super_light" style={{width: '120px', color: 'black'}}>Node Cost: 1</p>
            <p className="cell light" style={{width: '120px', color: 'black'}}>Node Cost: 5</p>
            <p className="cell medium" style={{width: '120px', color: 'black'}}>Node Cost: 10</p>
            <p className="cell heavy" style={{width: '120px', color: 'black'}}>Node Cost: 15</p>
            <p className="cell visited" style={{width: '120px', textAlign: 'center', color: 'black'}}>Visited</p>
            <p className="cell path" style={{width: '120px', textAlign: 'center', color: 'black'}}>Path</p>
          </div>
        </div>
        <div className="algorithms"  style={{marginBottom: '20px'}}>
            <div>
                <h3>BFS</h3>
                <div style={{marginBottom: '20px'}}>Nodes Visited: {bfsNodes}</div>
                <p style={{marginBottom: '20px'}}>Steps:</p>
                <Grid grid={bfsGridStep} />
                <p style={{marginBottom: '20px'}}>Solved Grid:</p>
                <Grid grid={solvedBfsGrid} />
                <div>Solve Time: {bfsTime}ms</div>
            </div>
            <div>
                <h3>DFS</h3>
                <div style={{marginBottom: '20px'}}>Nodes Visited: {dfsNodes}</div>
                <p style={{marginBottom: '20px'}}>Steps:</p>
                <Grid grid={dfsGridStep} />
                <p style={{marginBottom: '20px'}}>Solved Grid:</p>
                <Grid grid={solvedDfsGrid} />
                <div>Solve Time: {dfsTime}ms</div>
            </div>
            <div>
                <h3>Dijkstra</h3>
                <div style={{marginBottom: '20px'}}>Nodes Visited: {dijkstraNodes}</div>
                <p style={{marginBottom: '20px'}}>Steps:</p>
                <Grid grid={dijkstraGridStep} />
                <p style={{marginBottom: '20px'}}>Solved Grid:</p>
                <Grid grid={solvedDijkstraGrid} />
                <div>Solve Time: {dijkstraTime}ms</div>
            </div>
            <div>
                <h3>A*</h3>
                <div style={{marginBottom: '20px'}}>Nodes Visited: {astarNodes}</div>
                <p style={{marginBottom: '20px'}}>Steps:</p>
                <Grid grid={astarGridStep} />
                <p style={{marginBottom: '20px'}}>Solved Grid:</p>
                <Grid grid={solvedAstarGrid} />
                <div>Solve Time: {astarTime}ms</div>
            </div>
        </div>
        <div style={{fontWeight: 'bold', fontSize: '24px', marginTop: '20px'}}>Best Algorithm: {winner}</div>
      </>
    )
}

export default App;