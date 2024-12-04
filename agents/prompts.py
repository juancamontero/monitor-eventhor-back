ONBOARDING_PROMPT = """
A user is interested in tracking a specific topic, such as the performance of a sports team, geopolitical events in a region, or business/financial developments. Your task is to generate 6 to 10 diverse and specific forecasting questions based on their interest. Each question should focus on predicting the probability of a relevant event happening by a certain date, typically over a 1- to 12-month horizon. The questions should vary in type (e.g., probable events, disruptive events, trends, or thresholds) to ensure comprehensive coverage. Follow these steps:
	0.	Your knowledge cutoff is October 2023. The current date is {now_date}
	1.	Understand the User's Interest: Ask the user to provide details on their area of interest:
	  - What is the topic they want to monitor?
	  - Are there specific actors, trends, or events that they consider most important?
	  - What is the timeframe they are interested in?
	2.	Identify Key Actors and Drivers: Based on the topic, list the key actors, actions, and external factors that could significantly influence outcomes. For example, for a sports team, this could include player performance, injuries, coaching changes, or rival teams. For a geopolitical event, it might involve countries, military actions, or trade policies.
	3.	Break the Topic into Event Types: Break down the topic into different event types, including:
	  - Disruptive events: Sudden changes that could shift probabilities.
	  - Trend-driven events: Outcomes tied to ongoing developments.
	  - Milestone events: Important dates when a specific outcome is expected.
	4.	Generate Specific Questions: For each event type, create forecasting questions. Each question should:
	  - Predict the likelihood of a specific event happening by a certain date.
	  - Consider various dimensions like the actions of key actors, changes in trends, and external factors.
	  - Incorporate diversity, including probable events, low-probability but high-impact events, and trend-based predictions.
	5.	Specify the Timeframe: For each question, determine a specific timeframe (e.g., “within 3 months,' “by [specific date]') based on the user's interest and todays current date: {now_date}
	6.	The user's stated area of interest will be delimited with {delimiter} characters.


Sample Question: {delimiter}Geopolitical Events in the South China Sea{delimiter}:
	1.	Disruptive event:
	  - 'By July 1st, 2025, will China deploy any new military installations on artificial islands in the South China Sea?'
	2.	Trend-driven event:
	  - 'Will there be a 10 percent of increase in reported naval confrontations between China and the U.S. in the South China Sea by the end of Q1 2025?'

Output a json objet whit the following structure:


  "user_topic": "<User interest>",
  "actors": "<specific actors>"
  "questions": list of json objects, where each object has the following structure:
  					"event_type": "<Event type>", "question": "<Question>" 
 
Ensure:
1.	The user_topic field contains the user's main area of interest.
2.	The questions array contains objects, each with:
		- event_type: the event type associated with each question.
		- question: the question text itself.
3.	Check that the output JSON has the opening brackets and closing brackets before generating the final output 
Output only the JSON object in the format above, without additional explanations or commentary.
"""

DELIMITER="####"


