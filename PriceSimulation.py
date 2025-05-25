from math import comb


class PriceSimulation:

    def __init__(self, N, delta, q, P_0):
        """
        Initializes the PriceSimulation with the given parameters.

        :param N: Number of time steps
        :param delta: Maximum absolute price fluctuation per day
        :param q: Probability of price increase
        :param P_0: Initial price
        """
        self.N = N
        self.delta = delta
        self.q = q
        self.P_0 = P_0
        self.T = list(range(1, N + 1))
        self.A = ["wait", "buy"]  # wait, buy
        self.S = self.generate_states()

    def generate_states(self) -> list:
        """
        Generates the states of the price simulation.

        :param T: List of time points
        :param delta: Maximum absolute price fluctuation per day
        :param P_0: Initial price
        :return: List of states
        """
        daily_price_range = {
            1: [self.P_0]
        }  # Initialize the first day's price range with P_0

        # Generate the price ranges for each day
        for t in self.T[1:]:
            previous_price_range = daily_price_range[t - 1]
            current_price_range = []
            for price in previous_price_range:
                for k in range(0, 2 * self.delta + 1):
                    current_price_range.append(max(0, price + k - self.delta))
            current_price_range = list(set(current_price_range))
            daily_price_range[t] = current_price_range
        self.daily_price_range = daily_price_range

        # Flatten the daily price ranges into a list of states
        states = ["0"]  # "0" is the terminal state
        for t in self.T:
            for price in self.daily_price_range[t]:
                states.append((t, price))
        return states

    def get_possible_actions(self, state) -> list:
        """
        Returns the possible actions for a given state.

        :param state: The current state
        :return: List of possible actions
        """
        if state != "0" and state[0] == self.N:
            return [self.A[1]]  # Only buy in the last time step
        else:
            return self.A

    def get_possible_next_states(self, state, action) -> list:
        """
        Returns the possible next states given the current state and action.

        :param state: The current state
        :param action: The action taken
        :return: List of possible next states
        """
        if state == "0" or (state != "0" and action == self.A[1]):
            return ["0"]
        elif state != "0" and action == self.A[0]:
            next_day = state[0] + 1
            return [(next_day, price) for price in self.daily_price_range[next_day]]

    def get_direct_cost(self, state, action):
        """
        Returns the direct cost of taking an action in a given state.

        :param state: The current state
        :param action: The action taken
        :return: Direct cost
        """
        if state != "0" and state[0] == self.N and action == self.A[0]:
            raise Exception("Cannot wait in the last time step")

        if state != "0" and action == self.A[1]:
            return state[1]
        else:
            return 0

    def get_transition_probability(self, current_state, action, next_state) -> float:
        """
        Returns the transition probability from the current state to the subsequent state given an action.

        :param current_state: The current state
        :param action: The action taken
        :param next_state: The subsequent state
        :return: Transition probability
        """
        if current_state == "0":
            if next_state == "0":
                return 1.0
            else:
                return 0.0
        elif current_state != "0" and action == self.A[1]:
            if next_state == "0":
                return 1.0
            else:
                return 0.0
        elif current_state != "0" and next_state != "0" and action == self.A[0]:
            if next_state[0] == current_state[0] + 1 and any(
                next_state[1] == max(0, current_state[1] + k - self.delta)
                for k in range(0, 2 * self.delta + 1)
            ):
                if next_state[1] == 0 and self.delta - current_state[1] >= 0:
                    return sum(
                        comb(2 * self.delta, m)
                        * self.q**m
                        * (1 - self.q) ** (2 * self.delta - m)
                        for m in range(0, self.delta - current_state[1] + 1)
                    )
                elif next_state[1] > 0:
                    return (
                        comb(
                            2 * self.delta,
                            next_state[1] - current_state[1] + self.delta,
                        )
                        * self.q ** (next_state[1] - current_state[1] + self.delta)
                        * (1 - self.q)
                        ** (self.delta - next_state[1] + current_state[1])
                    )
                else:
                    return 0.0
            else:
                return 0.0
        else:
            return 0.0
