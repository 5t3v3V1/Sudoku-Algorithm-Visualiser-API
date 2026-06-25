from validator import is_valid
import asyncio
valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

async def livesolver(grid, websocket, steps = None, moves = None):
        if moves is None:
            moves = 0

        empty_list = list(grid.find_zeros())
        if len(empty_list) == 0:
            return True, steps, moves
        
        position = empty_list[0]
        for value in valid_numbers:
            if is_valid(grid, position, value):
                grid.nodes[position].number = value
                await websocket.send_json({
                    "type": "step",
                    "board": grid.to_list()
                })

                await asyncio.sleep(0.05)
                moves += 1
                solved, moves = await livesolver(grid, websocket, moves)
                if solved:
                    return True, moves
                
                grid.nodes[position].number = 0
                await websocket.send_json({
                    "type": "step",
                    "board": grid.to_list()
                })
                
                await asyncio.sleep(0.05)
                moves += 1
            
        return False, moves