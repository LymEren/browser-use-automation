from dotenv import load_dotenv
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
from browser_use.browser.context import BrowserContextConfig

load_dotenv()


browser = Browser(
    config=BrowserConfig(
        headless=False, 
        disable_security=True,
        new_context_config=BrowserContextConfig(
            disable_security=True,
            minimum_wait_page_load_time=1, 
            maximum_wait_page_load_time=10,
            # no_viewport=True,
            browser_window_size={
                'width': 1920,
                'height': 1080,
            }
        ),
    )
)


async def main():
    agent = Agent(
        task="1- Navigate to '' "
             "2- Select prepaid mobile plan "
             "3- Select iphone 12 pro max device. And go next step",
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser,
        # browser_context=context,
        # controller=custom_controller,  # For custom tool calling
        # use_vision=True,  # Enable vision capabilities
        # save_conversation_path="logs/conversation"  # Save chat logs
    )
    result = await agent.run()
    print(result)


asyncio.run(main())
