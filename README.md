# Trellis To-Do App Project

## Phase 1
- In our inital chat last week, we spoke about how we can benchmark different LLM's
- We also spoke about how we can't just use universal benchmarks like MMLU as it doesn't account for specific tasks one wants to do
- For this specific To-Do app, the only thing that matters for the agent is tool calling, narrowing the research to "which open-source model is the most reliable tool-caller that fits within my specs?"
- But first I had to learn what "trees" actually were to do the research
    - Binary Tree: In lamens terms, it is a data structure and each node can only branch into 2 sub nodes
    ![alt text](image.png)
    - Abstract Syntax Tree: In lamens terms, a syntax tree doesn't just use bigger or smaller numbers to coordinate data, instead it uses a string or equation to connect data, grammatical structure of code or an expression
        - BFCL uses it to grade a function call by parsing the call into that tree and comparing its structure (function name, argument names, values) against the expected one
    ![alt text](image-1.png)
### Finding the best benchmark
- After understanding data trees, I found the Berkeley Function Calling Leaderboard (BFCL). Built to asses the tool calling capabilities, more speicifcally the ability to invoke functions using a syntax tree method with more than 2k questions
- A more indepth one rather than just straight tool calling is the tau-bench, which actually uses full conversations emulating whole conversations between a user and a agent, it tests based of natural language form humans, the ability to follow guidelines and rules. 

### So which model should I use?
- Considering my specs as im running this model locally (4070 super, ryzen 7700x, 32gb 6000mhz ram DDR5)
- From the two bench marks(only looking at fc benchmarks)

#### BFCL
![Qwen3-8B (FC) | Overall Acc: 42.57 | Rank 39](image-2.png)
![Qwen3-14B (FC) | Overall Acc: 41.03 | Rank 43](image-3.png)
![Llama-3.1-8B-Instruct (Prompt, disregard) | Overall Acc: 25.83 | Rank 85](image-4.png)
![Llama-3.2-3B-Instruct (FC) | Overall Acc: 21.95 | Rank 98](image-5.png)
![Ministral-8B-Instruct-2410 (FC) | Overall Acc: 11.1 | Rank 105](image-6.png)
![phi4-mini](image-8.png)
- GLM-4.6 / Kimi K2 (FC) won't run on my machine
#### Tau0 Bench(even though for industry standards still helpful for learning)
- Proprietary (ceiling, cannot run locally):
    - Claude Sonnet 4.5: 88.1
    - GPT-5: 84.2
    - Gemini 2.5 Pro: 65.4
- Open source:
    - GLM-4.6: 75.9
    - Kimi K2-thinking: 75.2
    - DeepSeek V3.1: 42.8
    - Qwen3-32B: 41.5
- even the best models top out at 88
![alt text](image-9.png)
Berkeley Function Calling Leaderboard (BFCL): Patil et al., 2025, "The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models," ICML 2025. https://gorilla.cs.berkeley.edu/leaderboard.html

tau-bench: Yao et al., 2024, "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains," arXiv:2406.12045. Successor tau2-bench: Barres et al., 2025, arXiv:2506.07982. Leaderboard at https://taubench.com


### But is it enough
- Because public leaderboards measure much harder, different tasks on someone else's hardware, so running our own benchmark is the only way to get real numbers for our specific to-do agent on our specific machine
![alt text](image-7.png)
#### explaining the benchmark code
- The benchmark first starts with connecting to local Ollama through openai library which is pointed at the local host
- The makeTool takes a tool's name and descipriton, and returns it to the shape that ollama requires so the four tools get built the same way every time for consistancy
- models to test, one shared systemPrompt, a tools menu of 4 actions, and testCases (prompt paired with the tool that should fire, None means no tool)
- The ask function sends three things being the system prompt, the user prompt, and the tools menu, with a temperature of 0(greedy) making sure the answers are constiant and there are no outliers, then it checks if the model chose a tool and if so which one
- runs is set to 3 being how many times each prompt gets asked, so one lucky or unlucky answer doesnt decide the whole score
- For each model it first warms up with a throwaway "hi" so the loading time doesnt count, then starts a timer and asks every prompt 3 times, adding a point each time the model picks the correct tool
- At the end it works out the accuracy being correct out of total attempts, and the seconds it took, then prints them and saves everything to results.json
- So each model was benchmarked by asking it the same prompts several times and measuring two things, how often it picked the right tool (accuracy) and how long it took (speed)
#### results
- The original benchmark ran each prompt only once (runs = 1)
- The problem was that one prompt could decide a whole ranking, so a single lucky or unlucky answer would set the score and you couldnt tell a real result from a fluke
- To fix it I set runs to 3 so each prompt gets asked three times and every attempt counts towards the accuracy
- After running 3 times the accuracy came out exactly the same for every model (100, 75, 91.7, 66.7, 75), which showed the models were actually consistant at temperature 0 and the single run numbers were not luck after all
- The only real difference was the time, which roughly tripled (qwen3:8b went from about 40s to 102s, and qwen3:14b from 51s to 144s) since each prompt was now being asked three times instead of once
- So running it 3 times didnt change the ranking
- using qwen over llama cause accuracy is more important than time for a todo app
![alt text](image-10.png)
![alt text](image-11.png)
![alt text](image-12.png)