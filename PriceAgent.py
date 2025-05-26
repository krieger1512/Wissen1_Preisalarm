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
            for i in self.sim.S:
                expected_costs = {}
                for a in self.sim.get_possible_actions(i):
                    expected_costs[a] = sum(
                        self.sim.get_transition_probability(i, a, j)
                        * (self.sim.get_direct_cost(i, a) + self.gamma * V[j])
                        for j in self.sim.get_possible_next_states(i, a)
                    )
                new_V[i] = min(expected_costs.values())
            if all(abs(new_V[state] - V[state]) < 1e-6 for state in self.sim.S):
                break
            else:
                V = new_V.copy()
                update_count += 1
        print(f"\tFinished learning with {update_count} iterations.")
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
            policy[i] = min(expected_costs, key=expected_costs.get)
        return policy


def run_sim(N, delta, P_0):
    """ """
    print(f"Running simulation for N = {N}, delta = {delta}, and P_0 = {P_0} ...")
    sim = PriceSimulation(N, delta, P_0)
    # print("\tTotal Number of States:", len(sim.S))
    # print("\tDaily Price Range:", sim.daily_price_range)

    agent = PriceAgent(simulation=sim)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    sim_dir = os.path.join(current_dir, f"{N}_{delta}_{P_0}")
    os.makedirs(sim_dir, exist_ok=True)

    print("\tStarting Value Iteration ...")
    optimal_V = agent.learn_optimal_value_function()
    with open(os.path.join(sim_dir, "optimal_V.txt"), "w") as f:
        for state, v in optimal_V.items():
            f.write(f"{state}: {v}\n")
    print("\tOptimal value function learned and saved.")

    print("\tExtracting optimal policy ...")
    optimal_policy = agent.extract_optimal_policy(optimal_V)
    with open(os.path.join(sim_dir, "optimal_policy.txt"), "w") as f:
        for state, action in optimal_policy.items():
            f.write(f"{state}: {action}\n")
    print("\tOptimal policy extracted and saved.\n")


if __name__ == "__main__":
    # Param range
    N_range = [21, 42]
    delta_range = [5, 10]
    P_0_range = [150, 300, 600]

    for N in N_range:
        for delta in delta_range:
            for P_0 in P_0_range:
                run_sim(N, delta, P_0)
