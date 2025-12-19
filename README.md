
# Connect Four with Reinforcement Learning


<div align="left">
<p>
This project explores how different types of players perform at the game of Connect Four,
including human players, brute-force algorithms, and a reinforcement learning–based AI agent.
We investigate whether an AI can outperform humans, how it compares to brute-force Minimax
strategies, and whether the choice of training opponent affects learning.
</p>

<div align="center">
<img
  src="https://github.com/user-attachments/assets/464074a1-05de-4fa0-a113-14460ee9357e"
  width="507"
  height="367"
  alt="Training performance of AI agent against a random player"
/>

<p><em>
We had two AI players train against each other over the course of 300000 games. Players initially start out inexperienced and make random moves. As the game progress, the probabilities of each player winning individually goes to 0 and the probability of ties goes to 1.
</em></p>

</div>


---

## Project Overview

Inspired by the AlphaGo documentary, this project applies **reinforcement learning** to a simplified **4×4 Connect Four** environment. We implemented and compared four types of players:

- **Human player** (via GUI)
- **Random player**
- **Brute Force player** (Minimax with varying depths)
- **AI player** using **Tabular Q-learning**



---

## Key Research Questions

- Can an AI agent beat a human at Connect Four?
- Can an AI agent compete with or outperform a brute-force Minimax player?
- Does it matter who the AI agent is trained against (random vs AI vs brute force)?

---

## Player Types

### Random Player
- Chooses a random valid move.
- Serves as a baseline and as a training opponent.

### Brute Force Player (Minimax)
- Uses the Minimax algorithm to evaluate future board states.
- Tested at multiple depths (e.g., 1, 6, 11).
- Strong performance but computationally expensive at higher depths.

### AI Player (Reinforcement Learning)
- Uses **Tabular Q-learning** to learn state–action values.
- Learns by playing thousands of games and updating values using the **Bellman equation**.
- After training, selects moves that maximize expected reward.

---

## Training the AI Agent

- AI agents were trained over **tens to hundreds of thousands of games**.
- Training setups included:
  - AI vs AI
  - AI vs Random
- As training progressed:
  - AI vs AI converged toward mostly ties.
  - AI vs Random converged toward near-certain AI wins.
- Training against brute-force players was impractical due to runtime costs.

---

## Results and Conclusions

- The **AI player outperforms human players** most of the time.
- Humans playing first have a slight advantage; humans playing second rarely win.
- The AI **beats shallow Minimax players** and **ties with deeper Minimax players**, while taking a fraction of the computation time.
- Training against a **random player is nearly as effective** as training against another AI agent.

Overall, the AI player provides the best balance of performance and efficiency.


---


