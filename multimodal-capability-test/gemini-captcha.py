import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

from browser_use import Agent, ChatGoogle

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
	raise ValueError('GOOGLE_API_KEY is not set')

from browser_use.browser import BrowserProfile, BrowserSession

browser_profile = BrowserProfile(headless=False)
browser_session = BrowserSession(browser_profile=browser_profile)


async def run_search():
	llm = ChatGoogle(model='gemini-flash-latest', api_key=api_key)
	agent = Agent(
		llm=llm,
		task='Go to https://captcha.com/demos/features/captcha-demo.aspx and solve the captcha until success.',
		flash_mode=True,
		use_vision=True,
		browser_session=browser_session
	)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(run_search())