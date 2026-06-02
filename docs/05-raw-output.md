
```batch
PYTHONPATH=src python -m agentic.run_demo --mode single
```

```bat
user_proxy (to assistant):

Use the calculator tool with expression '12 * 7 + 3' and reply with only the number.

--------------------------------------------------------------------------------
assistant (to user_proxy):

***** Suggested tool call (call_gYt3k4VuoUCDfvqEZ1vebtd6): calculator *****
Arguments: 
{"expression":"12 * 7 + 3"}
***************************************************************************

--------------------------------------------------------------------------------

>>>>>>>> EXECUTING FUNCTION calculator...
Call ID: call_gYt3k4VuoUCDfvqEZ1vebtd6
Input arguments: {'expression': '12 * 7 + 3'}

>>>>>>>> EXECUTED FUNCTION calculator...
Call ID: call_gYt3k4VuoUCDfvqEZ1vebtd6
Input arguments: {'expression': '12 * 7 + 3'}
Output:
87.0
user_proxy (to assistant):

***** Response from calling tool (call_gYt3k4VuoUCDfvqEZ1vebtd6) *****
87.0
**********************************************************************

--------------------------------------------------------------------------------
assistant (to user_proxy):

87.0

--------------------------------------------------------------------------------
user_proxy (to assistant):



--------------------------------------------------------------------------------
assistant (to user_proxy):

It seems there was no input. How can I assist you today?

--------------------------------------------------------------------------------
user_proxy (to assistant):



--------------------------------------------------------------------------------
assistant (to user_proxy):

Please provide an expression or question for me to assist you with.

--------------------------------------------------------------------------------

>>>>>>>> TERMINATING RUN (31f307c4-e4bc-45f5-95d9-14f01f5df144): Maximum number of consecutive auto-replies reached
[Confident AI Trace Log]  No Confident AI API key found. Skipping trace posting.
Wrote evaluations/outputs/single_trace.json
```

```batch
PYTHONPATH=src python -m agentic.run_demo --mode multi
```

```bat
user_proxy (to assistant):

Call city_info with city Paris, then call budget_estimator with days=3 and daily_budget=200. Reply with a short summary that mentions the city highlight and the total budget.

--------------------------------------------------------------------------------
assistant (to user_proxy):

***** Suggested tool call (call_CSDd6LnCPrMYsl640q027O2C): city_info *****
Arguments: 
{"city": "Paris"}
**************************************************************************
***** Suggested tool call (call_jyh1HQ6OgPGhpUXW8K55NPHm): budget_estimator *****
Arguments: 
{"days": 3, "daily_budget": 200}
*********************************************************************************

--------------------------------------------------------------------------------

>>>>>>>> EXECUTING FUNCTION city_info...
Call ID: call_CSDd6LnCPrMYsl640q027O2C
Input arguments: {'city': 'Paris'}

>>>>>>>> EXECUTED FUNCTION city_info...
Call ID: call_CSDd6LnCPrMYsl640q027O2C
Input arguments: {'city': 'Paris'}
Output:
{'country': 'France', 'highlight': 'Louvre Museum'}

>>>>>>>> EXECUTING FUNCTION budget_estimator...
Call ID: call_jyh1HQ6OgPGhpUXW8K55NPHm
Input arguments: {'days': 3, 'daily_budget': 200}

>>>>>>>> EXECUTED FUNCTION budget_estimator...
Call ID: call_jyh1HQ6OgPGhpUXW8K55NPHm
Input arguments: {'days': 3, 'daily_budget': 200}
Output:
{'total_budget': 600}
user_proxy (to assistant):

***** Response from calling tool (call_CSDd6LnCPrMYsl640q027O2C) *****
{'country': 'France', 'highlight': 'Louvre Museum'}
**********************************************************************

--------------------------------------------------------------------------------
***** Response from calling tool (call_jyh1HQ6OgPGhpUXW8K55NPHm) *****
{'total_budget': 600}
**********************************************************************

--------------------------------------------------------------------------------
assistant (to user_proxy):

Your trip to Paris, known for its highlight, the Louvre Museum, will have a total budget of $600 for 3 days at a daily expense of $200.

--------------------------------------------------------------------------------
user_proxy (to assistant):



--------------------------------------------------------------------------------
assistant (to user_proxy):

It seems there's no additional input or request from you. How can I assist you further?

--------------------------------------------------------------------------------
user_proxy (to assistant):



--------------------------------------------------------------------------------
assistant (to user_proxy):

***** Suggested tool call (call_egKm3kh0D7HaMc2lgRFnwd32): city_info *****
Arguments: 
{"city":"Paris"}
**************************************************************************

--------------------------------------------------------------------------------

>>>>>>>> EXECUTING FUNCTION city_info...
Call ID: call_egKm3kh0D7HaMc2lgRFnwd32
Input arguments: {'city': 'Paris'}

>>>>>>>> EXECUTED FUNCTION city_info...
Call ID: call_egKm3kh0D7HaMc2lgRFnwd32
Input arguments: {'city': 'Paris'}
Output:
{'country': 'France', 'highlight': 'Louvre Museum'}
user_proxy (to assistant):

***** Response from calling tool (call_egKm3kh0D7HaMc2lgRFnwd32) *****
{'country': 'France', 'highlight': 'Louvre Museum'}
**********************************************************************

--------------------------------------------------------------------------------
assistant (to user_proxy):

***** Suggested tool call (call_DLQHxZQUm9YRBSABvUq7dgl3): budget_estimator *****
Arguments: 
{"days":3,"daily_budget":200}
*********************************************************************************

--------------------------------------------------------------------------------

>>>>>>>> TERMINATING RUN (f2836427-7b9e-4dd2-b07c-df5e5ad3f3d1): Maximum number of consecutive auto-replies reached
[Confident AI Trace Log]  No Confident AI API key found. Skipping trace posting.
Wrote evaluations/outputs/multi_trace.json
```