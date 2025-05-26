# %%
from PriceSimulation import PriceSimulation
import os


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
            policy[i] = (
                str(expected_costs)
                + " => "
                + min(expected_costs, key=expected_costs.get)
            )
        return policy


def run_sim(N, delta, P_0, fixed_q):
    """
    Runs a price simulation with the given parameters and saves the optimal value function and policy.

    :param N: Number of days in the simulation
    :param delta: Maximum price fluctuation per day
    :param P_0: Initial product price
    """
    print(f"Running price simulation:")
    print("  *  Parameters:")
    print(f"     ├── N = {N} days")
    print(f"     ├── delta = {delta}€ (maximum price fluctuation per day)")
    print(f"     ├── P_0 = {P_0}€ (initial product price)")
    print(
        f"     └── fixed_q = {fixed_q} (Probability for price increase/decrease is{' ' if fixed_q else ' not '}fixed)"
    )
    sim = PriceSimulation(N, delta, P_0, fixed_q)
    print("  *  Total Number of States:", len(sim.S))
    # print("  *  Daily Price Range:", sim.daily_price_range)

    agent = PriceAgent(simulation=sim)

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
    print(f"  *  Stored results in directory: {N}_{delta}_{P_0}_{fixed_q}\n")


if __name__ == "__main__":
    # Run simulations with different parameters
    run_sim(N=42, delta=5, P_0=300, fixed_q=True)
    run_sim(N=10, delta=5, P_0=25, fixed_q=True)
# %%
