# 2026/1/2
## Recap
Web agent has three components:
1. agent
2. browser
3. LLM

The agent relies on the LLM to produce browser action instructions, which the agent then executes.

previous todo:
1. using static webcontent as the target
2. using llama 3.2 to process rendered web content

---

## envrionment setup
To better inspect how web agents behave, we moved
1. agent (browser-use) to local
2. browser (playwright) to local
3. LLM (qwen3qwen3-vl:8b, llama3.2-vision:11b) to A100 gpu server

this is achieved by
`ssh -L 11434:localhost:11434 boy@10.8.0.6` (CHANGE username and ip)

---

## trial
* three different models with vision capability
1. gemini
2. qwen3-vl:8b
3. llama3.2-vision:11b

* three different tasks
1. github_star: "How many stars does the browser-use repo have?"
2. csie_monitor_cpu: "Go to https://monitor.csie.ntu.edu.tw/ and give the cpu usage for all machines."
3. solve_captcha: "Go to https://captcha.com/demos/features/captcha-demo.aspx and solve the captcha until success."

---

## result
| Model \ Task | github_star | csie_monitor_cpu | solve_captcha |
|---|---|---|---|
| gemini | success | success  | success, gemini passed the captcha after 2 or 3 attempts |
| qwen3-vl:8b | success, but way more agent steps compared to gemini | failed, seems still can't handle dynamic content | failed, even failed to find how to input  |
| llama3.2-vision:11b | failed, can't even understand the instruction | failed, can't even understand the instruction | failed, can't even understand the instruction |

---

## reflections
1. successfully setup multimodal web agent
1. qwen3-vl:8b out performed llama3.2-vision:11b
1. qwen3-vl:8b and llama3.2-vision:11b are incapable to handle simple tasks
1. qwen3-vl:8b and llama3.2-vision:11b run relatively slow on our A100 gpu compared to gemini api

---

## next step
