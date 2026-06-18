const generate_solve_board_button = document.getElementById("generate_solve_board");
const generate_solve_grid_button = document.getElementById("generate_solve_grid");
const generated_board = document.getElementById("generated_board");
const solved_board = document.getElementById("solved_board");
const generated_grid = document.getElementById("generated_grid");
const bfs_type = document.getElementById("bfs_type");
const bfs_nodes = document.getElementById("bfs_nodes");
const bfs_grid = document.getElementById("bfs_grid");
const bfs_steps = document.getElementById("bfs_steps")
const bfs_time = document.getElementById("bfs_time");
const dfs_type = document.getElementById("dfs_type");
const dfs_nodes = document.getElementById("dfs_nodes");
const dfs_grid = document.getElementById("dfs_grid");
const dfs_steps = document.getElementById("dfs_steps")
const dfs_time = document.getElementById("dfs_time");
const dijkstra_type = document.getElementById("dijkstra_type");
const dijkstra_nodes = document.getElementById("dijkstra_nodes");
const dijkstra_grid = document.getElementById("dijkstra_grid");
const dijkstra_steps = document.getElementById("dijkstra_steps")
const dijkstra_time = document.getElementById("dijkstra_time");
const astar_type = document.getElementById("astar_type");
const astar_nodes = document.getElementById("astar_nodes");
const astar_grid = document.getElementById("astar_grid");
const astar_steps = document.getElementById("astar_steps")
const astar_time = document.getElementById("astar_time");
const winner = document.getElementById("winner");
const board_time = document.getElementById("board_time");



function format_board(board) {
    format = "";

    for (let row = 0; row < board.length; row ++) {
        for (let cell = 0;  cell < board[row].split("").length; cell ++) {
            format += `<div>${board[row].split("")[cell]}</div>`
        };
    };

    return format;
};

function format_grid(grid) {
    format = "";

    for (let row = 0; row < grid.length; row ++) {
        for (let cell = 0; cell < grid[row].split("").length; cell ++) {
            format += `<div>${grid[row].split("")[cell]}</div>`
        };
    };

    return format
};

generate_solve_board_button.addEventListener("click", async () => {
    const response = await fetch("http://127.0.0.1:8000/generate_solve_board");

    const data = await response.json();

    console.log(data);
    generated_board.innerHTML = format_board(data.generated_board);
    solved_board.innerHTML = format_board(data.solved_board);
    board_time.innerText = `Solve Time: ${data.time_ms.toFixed(2)}ms`
})

generate_solve_grid_button.addEventListener("click", async () => {
    const response = await fetch("http://127.0.0.1:8000/generate_solve_grid");

    const data = await response.json();

    console.log(data);
    generated_grid.innerHTML = format_grid(data.generated_grid);
    bfs_type.innerHTML = "<h3>BFS</h3>";
    bfs_nodes.innerText = `Nodes Visited: ${data.bfs.bfs_nodes}`;
    bfs_grid.innerHTML = `Solved Grid: ${format_grid(data.bfs.solved_bfs_grid)}`;
    bfs_steps.innerText = `Steps: ${data.bfs.bfs_steps.length}`;
    bfs_time.innerText = `Solve Time: ${data.bfs.time_ms.toFixed(2)}ms`;
    dfs_type.innerHTML = "<h3>DFS</h3>";
    dfs_nodes.innerText = `Nodes Visited: ${data.dfs.dfs_nodes}`;
    dfs_grid.innerHTML = `Solved Grid: ${format_grid(data.dfs.solved_dfs_grid)}`;
    dfs_steps.innerText = `Steps: ${data.dfs.dfs_steps.length}`;
    dfs_time.innerText = `Solve Time: ${data.dfs.time_ms.toFixed(2)}ms`;
    dijkstra_type.innerHTML = "<h3>Dijkstra</h3>";
    dijkstra_nodes.innerText = `Nodes Visited: ${data.dijkstra.dijkstra_nodes}`;
    dijkstra_grid.innerHTML = `Solved Grid: ${format_grid(data.dijkstra.solved_dijkstra_grid)}`;
    dijkstra_steps.innerText = `Steps: ${data.dijkstra.dijkstra_steps.length}`;
    dijkstra_time.innerText = `Solve Time: ${data.dijkstra.time_ms.toFixed(2)}ms`;
    astar_type.innerHTML = "<h3>A*</h3>";
    astar_nodes.innerText = `Nodes Visited: ${data.astar.astar_nodes}`;
    astar_grid.innerText = `Solved Grid: ${format_grid(data.astar.solved_astar_grid)}`;
    astar_steps.innerText = `Steps: ${data.astar.astar_steps.length}`;
    astar_time.innerText = `Solve Time: ${data.astar.time_ms.toFixed(2)}ms`;

    const results = [
        {name: "BFS", time: data.bfs.time_ms},
        {name: "DFS", time: data.dfs.time_ms},
        {name: "Dijkstra", time: data.dijkstra.time_ms},
        {name: "A*", time: data.astar.time_ms}
    ];

    results.sort((a,b) => a.time - b.time);

    winner.innerText = `Best Algorithm: ${results[0].name}`;
})