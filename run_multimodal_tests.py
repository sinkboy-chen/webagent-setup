import argparse
import asyncio
import os
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent


def _load_env_from_script_dir() -> None:
	# Assumes ./.env exists next to this script and is exactly: GOOGLE_API_KEY=...
	key, value = (SCRIPT_DIR / ".env").read_text(encoding="utf-8").strip().split("=", 1)
	os.environ[key] = value


def _build_llm(model: str):
	if model == "gemini":
		from browser_use import ChatGoogle

		return ChatGoogle(model="gemini-flash-latest", api_key=os.environ["GOOGLE_API_KEY"])

	if model in {"qwen3-vl:8b", "llama3.2-vision:11b"}:
		from browser_use import ChatOllama

		return ChatOllama(model=model)

	raise ValueError(f"Unknown model: {model}")


def _task_prompt(task: str) -> str:
	if task == "github_star":
		return "How many stars does the browser-use repo have?"
	if task == "csie_monitor_cpu":
		return "Go to https://monitor.csie.ntu.edu.tw/ and give the cpu usage for all machines."
	if task == "solve_captcha":
		return "Go to https://captcha.com/demos/features/captcha-demo.aspx and solve the captcha until success."
	raise ValueError(f"Unknown task: {task}")


async def run(task: str, model: str) -> None:
	from browser_use import Agent
	from browser_use.browser import BrowserProfile, BrowserSession

	llm = _build_llm(model)
	browser_session = BrowserSession(browser_profile=BrowserProfile(headless=False))

	agent = Agent(
		llm=llm,
		task=_task_prompt(task),
		flash_mode=True,
		use_vision=True,
		browser_session=browser_session,
	)

	await agent.run()


def _parse_args(argv: list[str]) -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		prog="run_multimodal_tests",
		description="Unified runner for multimodal capability tests (GitHub stars, CSIE monitor CPU, captcha solve).",
	)
	parser.add_argument(
		"--task",
		required=True,
		choices=["github_star", "csie_monitor_cpu", "solve_captcha"],
		help="Which task to run.",
	)
	parser.add_argument(
		"--model",
		required=True,
		choices=["gemini", "qwen3-vl:8b", "llama3.2-vision:11b"],
		help="Model to use. 'gemini' uses Google API; others use Ollama.",
	)
	return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
	_load_env_from_script_dir()

	args = _parse_args(sys.argv[1:] if argv is None else argv)

	asyncio.run(run(args.task, args.model))


if __name__ == "__main__":
	main()
