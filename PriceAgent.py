# %%
from PriceSimulation import PriceSimulation


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
        V = {state: 0 for state in self.sim.S}
        update_count = 0
        while True:
            new_V = {}
            for i in self.sim.S:
                expected_costs = {}
                for a in self.sim.get_possible_actions(i):
                    expected_costs[a] = sum(
                        self.sim.get_transition_probability(i, a, j)
                        * (self.sim.get_direct_cost(i, a) + self.gamma * V[j])
                        for j in self.sim.S
                    )
                new_V[i] = min(expected_costs.values())
            if all(abs(new_V[state] - V[state]) < 1e-6 for state in self.sim.S):
                break
            else:
                V = new_V
                update_count += 1
                print(f"\t{update_count}-th Iteration ...")
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
                    for j in self.sim.S
                )
            policy[i] = min(expected_costs, key=expected_costs.get)
        return policy


if __name__ == "__main__":
    # Example usage
    sim = PriceSimulation(N=42, delta=5, q=0.5, P_0=300)
    print("Total Number of States:", len(sim.S))
    print("Daily Price Range:", sim.daily_price_range)

    agent = PriceAgent(simulation=sim)

    print("Starting Value Iteration ...")
    optimal_V = agent.learn_optimal_value_function()
    print("Optimal value function learned.")

    print("Extracting optimal policy ...")
    optimal_policy = agent.extract_optimal_policy(optimal_V)
    with open(f"optimal_policy.txt", "w") as f:
        for state, action in optimal_policy.items():
            f.write(f"{state}: {action}\n")
    print("Optimal policy extracted and saved.")

# %%
