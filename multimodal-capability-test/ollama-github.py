import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from browser_use import Agent, ChatOllama

async def run_search():
	llm = ChatOllama(model='qwen3-vl:8b')
	agent = Agent(
		llm=llm,
		task='How many stars does the browser-use repo have?',
		flash_mode=True,
		use_vision=True
	)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(run_search())