import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from browser_use import Agent, ChatOllama

async def run_search():
	llm = ChatOllama(model='qwen3-vl:8b')
	agent = Agent(
		llm=llm,
		task='Go to https://monitor.csie.ntu.edu.tw/ and give the cpu usage for all machines.',
		flash_mode=True,
		use_vision=True
	)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(run_search())