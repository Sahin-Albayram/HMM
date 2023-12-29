# python 3.10

class State:
    def __init__(self):
        pass

class Filtering:
    def __init__(self,prob0,prob1,prob2,prob3,prob4,states):
        self.prob_rain = prob0 #prior probability of rain
        self.prob_rain_rain = prob1 #transition probability from rain to rain
        self.prob_sun_rain = prob2 #transition probability from no rain to rain
        self.prob_rain_umb = prob3 #emission probability from rain to umbrella
        self.prob_sun_umb = prob4 #emission probability from no-rain to umbrella
        self.states = states
        self.prior_matrix = [1-prob0,prob0]
        self.transition_matrix = [[1-prob2,prob2],[1-prob1,prob1]]
        self.emission_matrix = [[1-prob4,prob4],[1-prob3,prob3]] 

    def recursive_step(self,t,is_rainy):
        umb = self.states[t-1]
        if t != 0:
            return  self.emission_matrix[is_rainy][umb]*((self.recursive_step(t-1,1) * self.transition_matrix[1][is_rainy])
                                                        +(self.recursive_step(t-1,0) * self.transition_matrix[0][is_rainy]))
        if t == 0:
            return self.prior_matrix[is_rainy]#*self.emission_matrix[is_rainy][umb]
    
    def process(self):
        self.result_rain = self.recursive_step(len(self.states),1)
        self.result_no_rain = self.recursive_step(len(self.states),0)

        norm_factor = self.result_rain + self.result_no_rain
        self.result_rain /= norm_factor
        self.result_no_rain /= norm_factor

        print(round(self.result_rain,2))
        print(round(self.result_no_rain,2))


filter = Filtering(0.5,0.7,0.3, 0.9, 0.2,[1,1])
filter.process()

# class Filtering:
#     def __init__(self, prob0, prob1, prob2, prob3, prob4, states):
#         self.prob_rain = prob0  # prior probability of rain
#         self.prob_rain_rain = prob1  # transition probability from rain to rain
#         self.prob_sun_rain = prob2  # transition probability from no rain to rain
#         self.prob_rain_umb = prob3  # emission probability from rain to umbrella
#         self.prob_sun_umb = prob4  # emission probability from no-rain to umbrella
#         self.states = states
#         self.prior_matrix = [1 - prob0, prob0]
#         self.transition_matrix = [[1 - prob2, prob2], [1 - prob1, prob1]]
#         self.emission_matrix = [[1 - prob4, prob4], [1 - prob3, prob3]]
#         self.memo = {}

#     def recursive_step(self, t, is_rainy):
#         # Check if we have already computed this
#         if (t, is_rainy) in self.memo:
#             return self.memo[(t, is_rainy)]
        
#         # Base case: start of the sequence
#         if t == 0:
#             result = self.prior_matrix[is_rainy]
#         else:
#             # Get the observation at time t-1 (0 for no umbrella, 1 for umbrella)
#             umb = self.states[t-1]
#             result = self.emission_matrix[is_rainy][umb] * (
#                 (self.recursive_step(t-1, 1) * self.transition_matrix[1][is_rainy]) +
#                 (self.recursive_step(t-1, 0) * self.transition_matrix[0][is_rainy]))
        
#         # Store the result in the memo dictionary
#         self.memo[(t, is_rainy)] = result
#         return result

#     def process(self):
#         self.result_rain = self.recursive_step(len(self.states), 1)
#         self.result_no_rain = self.recursive_step(len(self.states), 0)
        
#         # Normalize the results
#         norm_factor = self.result_rain + self.result_no_rain
#         self.result_rain /= norm_factor
#         self.result_no_rain /= norm_factor

#         print("Probability of rain:", self.result_rain)
#         print("Probability of no rain:", self.result_no_rain)


# filter = Filtering(0.5, 0.7, 0.3, 0.9, 0.2, [1, 1])
# filter.process()
