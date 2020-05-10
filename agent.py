from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import save_model, load_model
import numpy as np
import random
from collections import deque

ACTIONS = 2
MEMORY_SIZE = 1024
BATCH_SIZE = 128
FEATURE_SIZE = 5
# MIN_STEPS = 30
GAMMA = 0.975
OBSERVE_PERIOD = 256

class Agent:

    def __init__(self, load_weights=False):
        self.load_weights = load_weights
        self.memory = deque()
        self.steps = 0

        if not self.load_weights:
            self.model = Sequential()
            self.model.add(Dense(32, activation='relu', input_dim=FEATURE_SIZE))
            self.model.add(Dense(16, activation='relu'))
            self.model.add(Dense(ACTIONS, activation='linear', kernel_initializer='he_normal'))
            self.model.compile(loss='mse', optimizer='adam')
        else:
            self.model = load_model('rl_best_agent.h5')

    def get_prediction(self, state):

        result = self.model.predict(state)
        print(result)
        best = np.argmax(result)
        return best

    def get_sample(self, sample):
        self.memory.append(sample)
        self.steps = self.steps + 1
        if(len(self.memory) > MEMORY_SIZE):
            self.memory.popleft()

    def backward(self):

        if self.steps > OBSERVE_PERIOD and not self.load_weights:
            sample = random.sample(self.memory, BATCH_SIZE)
            inputs = np.zeros((BATCH_SIZE, FEATURE_SIZE))
            targets = np.zeros((inputs.shape[0], ACTIONS))

            for i, mini_batch in enumerate(sample):
                state_t0 = mini_batch[0]
                action_t0 = mini_batch[1]
                reward_t0 = mini_batch[2]
                state_t1 = mini_batch[3]

                inputs[i:i + 1] = state_t0
                prediction = self.model.predict(state_t0)

                # print("prediction: ", prediction)

                targets[i] = prediction
                q_sa = self.model.predict(state_t1)

                if state_t1 is not None:
                    targets[i, action_t0] = reward_t0 + GAMMA * np.max(q_sa)
                else:
                    targets[i, action_t0] = reward_t0

            self.model.fit(inputs, targets, batch_size=BATCH_SIZE, epochs=1)



    def save_model_weights(self):
        save_model(self.model, "rl_agent_agent.h5")