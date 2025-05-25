from PriceSimulation import PriceSimulation


class PriceAgent:

    def __init__(self, simulation: PriceSimulation):
        """
        Initializes the PriceAgent with a PriceSimulation instance.

        :param simulation: An instance of PriceSimulation
        """
        self.simulation = simulation

    def get_possible_actions(self, state):
        """
        Returns the possible actions for a given state.

        :param state: The current state
        :return: List of possible actions
        """
        return self.simulation.A


if __name__ == "__main__":
    # Example usage
    sim = PriceSimulation(N=42, delta=5, q=0.5, P_0=300)
    print("Time Steps:", sim.T)
    print("Number of states:", len(sim.S))
    print("Daily Price Range:", sim.daily_price_range)
