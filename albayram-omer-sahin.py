# python 3.10

class HMM:
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

    def backward_recursive(self,t,is_rainy):
        
        if t == len(self.states)-1:
            return 1
        else:
            umb = self.states[t]
            return (self.transition_matrix[is_rainy][0] * self.emission_matrix[0][umb]* self.backward_recursive(t+1,0)+
                    self.transition_matrix[is_rainy][1] * self.emission_matrix[1][umb]* self.backward_recursive(t+1,1)) 



    def forward_recursive(self,t,is_rainy):
        umb = self.states[t-1]
        if t != 0:
        
            return  self.emission_matrix[is_rainy][umb]*((self.forward_recursive(t-1,1) * self.transition_matrix[1][is_rainy])
                                                        +(self.forward_recursive(t-1,0) * self.transition_matrix[0][is_rainy]))
        if t == 0:
            return self.prior_matrix[is_rainy]#*self.emission_matrix[is_rainy][umb]
    
    def filter_process(self,l):
        current_rain = self.forward_recursive(l,1)
        current_no_rain = self.forward_recursive(l,0)

        norm_factor = current_rain + current_no_rain
        current_rain /= norm_factor
        current_no_rain /= norm_factor
        return [round(current_rain,2),round(current_no_rain,2)]
        #print(f"<{round(current_rain,2)}, {round(current_no_rain,2)}>")

    def likelihood_process(self):
        current_rain = self.forward_recursive(len(self.states), 1)
        current_no_rain = self.forward_recursive(len(self.states), 0)

        likelihood = current_rain + current_no_rain
        return round(likelihood,2)
        #print(f"<{round(likelihood,2)}>")

    
    def smooth_process(self,k):

        forward_prob_no_rain = self.forward_recursive(k,0)
        forward_prob_rain = self.forward_recursive(k,1)

        fnorm = forward_prob_no_rain + forward_prob_rain
        
        forward_prob_rain = forward_prob_rain / fnorm
        forward_prob_no_rain = forward_prob_no_rain / fnorm

        backward_prob_no_rain = self.backward_recursive(k,0)
        backward_prob_rain = self.backward_recursive(k,1)


        smoothed_prob_no_rain = forward_prob_no_rain * backward_prob_no_rain
        smoothed_prob_rain = forward_prob_rain * backward_prob_rain
        
       
        norm_factor = smoothed_prob_no_rain + smoothed_prob_rain
        smoothed_prob_no_rain = smoothed_prob_no_rain / norm_factor
        smoothed_prob_rain = smoothed_prob_rain / norm_factor

        return (round(smoothed_prob_rain,2),round(smoothed_prob_no_rain,2))
        #print(f"<{smoothed_prob_rain}, {smoothed_prob_no_rain}>")
    def MLE(self):
        previous_probs = self.filter_process(1)
        probs = []
        path = []
        for i in range(1,len(self.states)):
            probs.append(previous_probs)
            bigger = 0
            if previous_probs[0] >= previous_probs[1]:
                bigger = 1
            path.append(bigger)
            
            current_probs = []
            pb = previous_probs[1-bigger]
            tm = self.transition_matrix[bigger][1]
            em = self.emission_matrix[1][self.states[i]]
            current_probs.append(round(pb*tm*em,2))
            pb = previous_probs[1-bigger]
            tm = self.transition_matrix[bigger][0]
            em = self.emission_matrix[0][self.states[i]]
            current_probs.append(round(pb*tm*em,2))
            previous_probs = current_probs
        bigger = 0
        if previous_probs[0] >= previous_probs[1]:
            bigger = 1
        probs.append(previous_probs)
        path.append(bigger)
        actual_path=[]
        for p in path:
            actual_path.append('T' if p == 1 else 'F')
        return (actual_path,probs)
            
inp = input("\n")
inp0 = inp.split("[")
inp0_0= inp0[0].split(" ")

inp0_1= inp0[1].split("]")[0].split(" ")
states = []
for s in inp0_1:
    if s == 'T':
        states.append(1)
    else:
        states.append(0)
hmm = HMM(float(inp0_0[0]),float(inp0_0[1]),float(inp0_0[2]),float(inp0_0[3]),float(inp0_0[4]),states)
type = inp0_0[5]

if type == "F":
    result = hmm.filter_process(len(hmm.states))
    print(f"<{result[0]}, {result[1]}>")
if type == "S":
    k = int(inp0[1].split("]")[1])
    result = hmm.smooth_process(k)
    print(f"<{result[0]}, {result[1]}>")
if type == "M":
    result = hmm.MLE()
    print(f"[",end="")
    for p in result[0]:
        print(f" {p}",end="")
    print("][",end="")
    for v in result[1]:
        print(f"<{v[0]}, {v[1]}>,",end="")
    print("]")
if type == "L":
    result = hmm.likelihood_process()
    print(f"<{result}>")




