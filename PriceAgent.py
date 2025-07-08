# %%
from PriceSimulation import PriceSimulation
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class PriceAgent:

    def __init__(self, simulation: PriceSimulation, gamma=1.0):
        """
        Initializes the PriceAgent with a PriceSimulation instance.

        :param simulation: An instance of PriceSimulation
        """
        self.sim = simulation
        self.gamma = gamma

    def learn_optimal_value_function(self) -> dict:
        """
        Learns the optimal value function for each state using the Value Iteration algorithm.
        """
        V = {state: 0 for state in self.sim.S if state != "0"}
        V["0"] = 0  # Terminal state has value 0
        update_count = 0
        while True:
            new_V = {}
            # temp = {}
            for i in self.sim.S:
                expected_costs = {}
                for a in self.sim.get_possible_actions(i):
                    expected_costs[a] = sum(
                        self.sim.get_transition_probability(i, a, j)
                        * (self.sim.get_direct_cost(i, a) + self.gamma * V[j])
                        for j in self.sim.get_possible_next_states(i, a)
                    )
                # temp[i] = expected_costs.copy()
                new_V[i] = min(expected_costs.values())
            if all(abs(new_V[state] - V[state]) < 1e-6 for state in self.sim.S):
                # print(f"     {temp}")
                break
            else:
                V = new_V.copy()
                # print(f"     {temp}")
                update_count += 1
        print(f"     ├── Finished learning with {update_count} iterations.")
        return V

    def extract_optimal_policy(self, optimal_V) -> dict:
        """
        Computes the optimal policy based on the learned value function.

        :param V: The learned value function
        :return: A dictionary mapping states to optimal actions
        """
        policy = {}
        for i in self.sim.S:
            expected_costs = {}
            for a in self.sim.get_possible_actions(i):
                expected_costs[a] = sum(
                    self.sim.get_transition_probability(i, a, j)
                    * (self.sim.get_direct_cost(i, a) + self.gamma * optimal_V[j])
                    for j in self.sim.get_possible_next_states(i, a)
                )
            min_expected_cost = min(expected_costs.values())
            policy[i] = (
                str(expected_costs)
                + " => "
                + str(
                    [
                        key
                        for key, value in expected_costs.items()
                        if value == min_expected_cost
                    ]
                )
            ).replace("'", "")
        return policy

    def visualize_policy(self, policy, sim_dir):
        """
        Visualizes the optimal policy and saves the visualization to the specified directory.

        :param policy: A dictionary mapping states to actions
        :param sim_dir: Directory to save the visualization
        """

        day_range = np.array(self.sim.T)
        price_range = np.array(self.sim.daily_price_range[self.sim.N])
        matrix_height = len(day_range)
        matrix_width = len(price_range)

        day_index = {day: i for i, day in enumerate(day_range)}
        price_index = {price: i for i, price in enumerate(price_range)}

        # Create matrices for states and actions
        state_matrix = np.full((matrix_height, matrix_width), "", dtype=object)
        action_matrix = np.full((matrix_height, matrix_width), -1)
        for state, decision in policy.items():
            if state != "0":
                state_day = state[0]
                state_price = state[1]
                state_matrix[day_index[state_day], price_index[state_price]] = (
                    f"{state_day}, {state_price}"
                )
                action = decision.split(" => ")[1].strip("[]").split(", ")
                if len(action) == 2:
                    action_matrix[day_index[state_day], price_index[state_price]] = 2
                elif len(action) == 1:
                    if action[0] == self.sim.A[0]:
                        action_matrix[
                            day_index[state_day], price_index[state_price]
                        ] = 0
                    elif action[0] == self.sim.A[1]:
                        action_matrix[
                            day_index[state_day], price_index[state_price]
                        ] = 1

        # Create a color matrix based on the action matrix and color map
        color_map = {
            -1: "white",  # No action
            0: "blue",  # Wait
            1: "orange",  # Buy
            2: "gray",  # Both actions
        }
        C_colors = np.empty((matrix_height, matrix_width, 3))
        for i in range(matrix_height):
            for j in range(matrix_width):
                C_colors[i, j] = mcolors.to_rgb(color_map[action_matrix[i, j]])

        # Plot the colored grid
        cell_size = 30.75 / max(matrix_height, matrix_width)  # in inches
        fig, ax = plt.subplots(
            figsize=(matrix_width * cell_size, matrix_height * cell_size)
        )
        ax.imshow(C_colors, extent=[0, matrix_width, 0, matrix_height])

        # Add state label to each cell
        for i in range(matrix_height):
            for j in range(matrix_width):
                text_color = "white" if action_matrix[i, j] == 0 else "black"
                ax.text(
                    j + 0.5,
                    len(day_range) - i - 0.5,
                    state_matrix[i, j],
                    va="center",
                    ha="center",
                    color=text_color,
                    fontsize=(cell_size * 0.9 if cell_size < 0.1 else 15 * cell_size),
                )

        # Set up gridlines and remove ticks
        ax.set_xticks(np.arange(matrix_width + 1))
        ax.set_yticks(np.arange(matrix_height + 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(color="black", linewidth=0.5)
        ax.set_xlim(0, matrix_width)
        ax.set_ylim(0, matrix_height)
        ax.invert_yaxis()  # To make row 0 appear at the top like a matrix
        plt.tight_layout()
        plt.savefig(
            os.path.join(sim_dir, "optimal_policy_visualization.jpg"),
            dpi=900,
            bbox_inches="tight",
        )


def run_sim(N, delta, P_0, fixed_q, gamma=1.0):
    """
    Runs a price simulation with the given parameters and saves the optimal value function and policy.

    :param N: Number of days in the simulation
    :param delta: Maximum price fluctuation per day
    :param P_0: Initial product price
    :param fixed_q: Whether to use fixed q
    :param gamma: Discount factor for future rewards
    """
    print(f"Running price simulation:")
    print("  *  Parameters:")
    print(f"     ├── N = {N} days")
    print(f"     ├── delta = {delta}€ (maximum price fluctuation per day)")
    print(f"     ├── P_0 = {P_0}€ (initial product price)")
    print(f"     └── fixed_q = {fixed_q} (q is{' ' if fixed_q else ' not '}fixed)")
    sim = PriceSimulation(N, delta, P_0, fixed_q)
    print("  *  Total Number of States:", len(sim.S))
    # print("  *  Daily Price Range:", sim.daily_price_range)

    agent = PriceAgent(simulation=sim, gamma=gamma)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    sim_dir = os.path.join(current_dir, f"{N}_{delta}_{P_0}_{fixed_q}")
    os.makedirs(sim_dir, exist_ok=True)

    print("  *  Starting Value Iteration ...")
    optimal_V = agent.learn_optimal_value_function()
    with open(os.path.join(sim_dir, "optimal_V.txt"), "w") as f:
        for state, v in optimal_V.items():
            f.write(f"{state}: {v}\n")
    print("     └── Optimal value function learned and saved.")

    print("  *  Extracting optimal policy ...")
    optimal_policy = agent.extract_optimal_policy(optimal_V)
    with open(os.path.join(sim_dir, "optimal_policy.txt"), "w") as f:
        for state, action in optimal_policy.items():
            f.write(f"{state}: {action}\n")
    print("     └── Optimal policy extracted and saved.")

    print("  *  Visualizing optimal policy ...")
    agent.visualize_policy(optimal_policy, sim_dir)
    print("     └── Visualization saved.")

    print(f"  *  Stored results in directory: {N}_{delta}_{P_0}_{fixed_q}\n")


if __name__ == "__main__":
    # Run simulations with different parameters

    run_sim(N=42, delta=5, P_0=300, fixed_q=True)
    run_sim(N=42, delta=5, P_0=300, fixed_q=False)

    run_sim(N=10, delta=4, P_0=20, fixed_q=True)
    run_sim(N=10, delta=4, P_0=20, fixed_q=False)
# %%
