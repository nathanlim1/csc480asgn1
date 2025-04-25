import sys
import heapq

moves = {  # Directions for movement
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}

def get_start_and_goals(grid):
    """Returns the start location and goal locations of a given grid."""
    start = None
    goals = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '@':
                start = (r, c)
            elif grid[r][c] == '*':
                goals.append((r, c))
    return start, goals

def dfs_search(grid, start, goals):
    """Performs a DFS on the grid. Returns the actions taken as a list, number of nodes generated
    and the number of nodes expanded."""
    init_state = (start, frozenset(goals))

    stack = [(init_state, [])]

    # Use to keep track of visited states to avoid cycles and infinite looping
    visited = set(init_state)

    nodes_generated = 1
    nodes_expanded = 0

    while stack:
        cur_state, actions = stack.pop()
        cur_loc = cur_state[0]
        cur_goals = cur_state[1]

        nodes_expanded += 1

        # Update remaining goals if the new location is a goal
        if cur_loc in cur_goals:
            actions = actions + ["V"]
            cur_goals = cur_goals - {cur_loc}

        # Check if all goals are reached
        if not cur_goals:
            return actions, nodes_generated, nodes_expanded

        # Get possible moves
        for direction in moves:
            new_loc = (cur_loc[0] + moves[direction][0], cur_loc[1] + moves[direction][1])
            if (0 <= new_loc[0] < len(grid) and
                0 <= new_loc[1] < len(grid[0]) and
                grid[new_loc[0]][new_loc[1]] != '#'):

                # Check for cycles
                proposed_state = (new_loc, cur_goals)

                if proposed_state not in visited:
                    visited.add(proposed_state)
                    stack += [(proposed_state, actions + [direction])]
                    nodes_generated += 1

    return None, nodes_generated, nodes_expanded

def ufs_search(grid, start, goals):
    """Performs a UFS on the grid. Returns the actions taken as a list, number of nodes generated,
    and the number of nodes expanded."""
    init_state = (start, frozenset(goals))

    q = []
    heapq.heapify(q)
    heapq.heappush(q, (0, init_state, []))  # (cost, state, actions)

    # Visited states are mapped to their lowest cost
    visited_best_costs = {
        init_state: 0
    }

    nodes_generated = 1
    nodes_expanded = 0

    while q:
        cost, cur_state, actions = heapq.heappop(q)
        cur_loc = cur_state[0]
        cur_goals = cur_state[1]

        if cost > visited_best_costs[cur_state]:
            continue

        nodes_expanded += 1

        # Update remaining goals if the new location is a goal
        if cur_loc in cur_goals:
            actions = actions + ["V"]
            cur_goals = cur_goals - {cur_loc}

        # Check if all goals are reached
        if not cur_goals:
            return actions, nodes_generated, nodes_expanded

        # Get possible moves
        for direction in moves:
            new_loc = (cur_loc[0] + moves[direction][0], cur_loc[1] + moves[direction][1])
            if (0 <= new_loc[0] < len(grid) and
                    0 <= new_loc[1] < len(grid[0]) and
                    grid[new_loc[0]][new_loc[1]] != '#'):

                # Check for cycles
                proposed_state = (new_loc, cur_goals)
                proposed_cost = cost + 1

                if (proposed_state not in visited_best_costs
                        or proposed_cost < visited_best_costs[proposed_state]):
                    visited_best_costs[proposed_state] = proposed_cost
                    heapq.heappush(q, (proposed_cost, proposed_state, actions + [direction]))
                    nodes_generated += 1

    return None, nodes_generated, nodes_expanded



def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py <algorithm> <world-file>")
        exit(1)

    algorithm = sys.argv[1]
    world_file = sys.argv[2]

    if algorithm not in ["depth-first", "uniform-cost"]:
        print("Invalid algorithm. Choose from: depth-first, uniform-cost")
        exit(1)

    try:
        with open(world_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File {world_file} not found.")
        exit(1)

    cols = int(lines[0].strip())
    rows = int(lines[1].strip())
    grid = [list(line.strip()) for line in lines[2:2+rows]]

    if len(grid[0]) != cols:
        print("Invalid world file: number of columns does not match.")
        exit(1)

    start, goals = get_start_and_goals(grid)

    if algorithm == "depth-first":
        path, gen, exp = dfs_search(grid, start, goals)
    else:
        path, gen, exp = ufs_search(grid, start, goals)

    if path is None:
        print("No solution")
    else:
        for a in path:
            print(a)

    print(f"{gen} nodes generated")
    print(f"{exp} nodes expanded")

if __name__ == "__main__":
    main()