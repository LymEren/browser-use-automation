from dotenv import load_dotenv
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
from browser_use.browser.context import BrowserContextConfig
from browser_use import Browser, Controller, ActionResult
import os
import re

load_dotenv()  # load environment variables from .env
def find_and_replace_xpath(file_path, variable_name, new_value):
    # Pattern to match lines that may contain the XPath variable assignment
    pattern = re.compile(rf'\b{re.escape(variable_name)}\b\s*=\s*["\'](.*?)["\']')
    print(f"File updater started.\nStarting to update '{variable_name}' in {file_path}")

    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    print("Read file successfully.")

    indentation = "    "  # 4 spaces
    # Replace the found XPath with the new one
    modified_lines = []
    foundFlag = False
    for line in lines:
        match = pattern.search(line)
        if match:
            foundFlag = True
            # Replace the old value with the new one
            modified_line = f'{indentation}{variable_name} = "{new_value}"\n'
            modified_lines.append(modified_line)
            print(f"Found and updated '{variable_name}'.")
        else:
            modified_lines.append(line)

    # Write the modified lines back to the file
    if not foundFlag:
        print(f"'{variable_name}' not found. No changes made.")
    else:
        # Write the modified lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(modified_lines)
        print(f"Updated '{variable_name}' successfully in {file_path}.")


os.environ["ANONYMIZED_TELEMETRY"] = "false"


load_dotenv()

browser = Browser(
    config=BrowserConfig(
        headless=False,  # This is True in production
        disable_security=True,
        new_context_config=BrowserContextConfig(
            disable_security=True,
            minimum_wait_page_load_time=1,  # 3 on prod
            maximum_wait_page_load_time=10,  # 20 on prod
            # no_viewport=True,
            browser_window_size={
                'width': 1920,
                'height': 1080,
            },
            # trace_path='./tmp/web_voyager_agent',
        ),
    )
)


websiteUrl = "file:///C:/Users/eyyub.eren/Downloads/yeni/CSR%20TOOLBOX.html"
locatorPath = "C:/Users/eyyub.eren/Desktop/ai_agents/locator199.py"  # Adjust the filename as needed
inoperativeXpath = "btn_b2c"

# clickable mı diye baksın
# baslangıcta bu haliyle bir calissin, etiotoda feedback alınabilir
# kullanıcı da kontrol edip feedback versin

async def main():
    agent = Agent(
        task=f"""Get XPath for the all elements in the website {websiteUrl}.

        Here are the specific steps:
        
        1. Go to {websiteUrl}."
        2. Analysis {inoperativeXpath} it in the website (do not click this element, if you click you will take connection error) 
        3. Get new xpath and write it in the result (dont write anything else).
         
        Collect Element Description: Ask the user for a description of the web page element they wish to find the XPath for. This description may include the element's text content, id, class name, or any other attribute.
        
        Construct XPath Query: Based on the description provided, construct an appropriate XPath query expression. In this construction process, you can use one or several of the following methods:
        
        Test XPath Expression: Verify that the constructed XPath expression selects the intended element by testing it.
        Return XPath to User: Once confirmed, return the XPath expression back to the user.
        
        Rules:
        - Write only xpath in the final result (dont write anything else)
        - Prefer to use //* for the start 
        - If you can use //*[contains(text(), '')] you can prefer to use it.
        - Wait for each element to load before interacting
        - Please get xpath like this style:
            txt_totalPlanAndStatus = "//*[contains(text(), 'Plans & Status')]" 
            lbl_dashboard = "//h1[normalize-space() = 'Dashboard']" 
            lbl_csrLoginPageText = "//*[normalize-space() = 'Login with your organizational account']" 
            btn_logout = "(//*[normalize-space() = 'B2C'])[1]/following-sibling::*[6]" 
            lbl_csrLogoutPageText = "//*[normalize-space() = 'You have been disconnected.']" 
            btn_login = "//button[normalize-space() = 'Login']"
            
        - You can use this parameters for finding xpath:
            - Ancestor example: //input[@id='searchInput']/ancestor::form
            - Siblings example: //h2[contains(text(), 'Introduction')]/following-sibling::p
            - Child example: //h2[contains(text(), 'Introduction')]/child::p 
            - /.. (Parent) example: //div[@id='content']/../..
            - /* (All Children) example: //body/*
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser,
        # browser_context=context,
        # controller=custom_controller,  # For custom tool calling
        # use_vision=True,  # Enable vision capabilities
        # save_conversation_path="logs/conversation"  # Save chat logs
    )
    result = await agent.run()
    result = result.final_result()
    renewedXpath = result

    print(result)

    find_and_replace_xpath(locatorPath, inoperativeXpath, renewedXpath)

asyncio.run(main())
