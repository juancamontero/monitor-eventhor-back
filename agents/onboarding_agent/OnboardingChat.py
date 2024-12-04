import json

from utils.parse_date import GOOGLE_SEARCH_DATE_FORMAT
from datetime import datetime


from agents.prompts import ONBOARDING_PROMPT, DELIMITER
from agents.llm_agent import get_llm_agent_class


class OnboardingAgent:
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        beforeTimestamp: int | None = None,
    ):
        self.model = model
        self.onboardingPrompt = ONBOARDING_PROMPT
        self.beforeTimestamp = beforeTimestamp
        self.today_string = datetime.now().strftime(GOOGLE_SEARCH_DATE_FORMAT)
        self.onboardingAgent = get_llm_agent_class(model)(
            model=model, temperature=0.0, max_tokens=512
        )

    async def completions(self, messages):
        # Step 1: Get the question from the last message
        if len(messages) == 0:
            raise ValueError("No messages provided")
        interest = messages[-1]["content"]
        onboarding_formatted_prompt = self.onboardingPrompt.format(
            delimiter=DELIMITER, now_date=self.today_string
        )
        onboarding_input = [
            {"role": "system", "content": onboarding_formatted_prompt},
            {"role": "user", "content": f"{DELIMITER}{interest}{DELIMITER}"},
        ]
        on_boarding_response = self.onboardingAgent.completions(onboarding_input)
        
        print(on_boarding_response)
        return json.dumps(on_boarding_response) 
