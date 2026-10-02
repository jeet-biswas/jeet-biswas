# JeetGPT: a hosted-model chat prototype

[Repository](https://github.com/jeet-biswas/chatbot) |
[Reviewed application source](https://github.com/jeet-biswas/chatbot/blob/1b4723e7f973f3a72b710e27afe6732b708cbebd/app.py)

This Python prototype connects a Streamlit chat interface to a Hugging Face model
endpoint through LangChain. The source configures `Meta-Llama-3-8B-Instruct` and
loads the access token from the environment.

## Request flow

1. A user enters a message in the Streamlit interface.
2. The application sends that input to the hosted model wrapper.
3. The returned response is displayed in the chat interface.
4. Session state retains messages for display during that session.

This is useful practice in connecting a UI, environment-based configuration,
and a hosted inference service. It does not involve training a language model.

## A distinction worth making

Visible chat history is not the same as model memory. In the reviewed code, the
model call receives the current message; the stored transcript is not passed as
conversation context. The application also does not implement document retrieval
or tool-calling agents.

## Next engineering steps

- Pass an explicit, bounded conversation history when continuity is required.
- Report unavailable endpoints and missing configuration clearly to the user.
- Complete dependency declarations: the reviewed requirements omit Streamlit.
- Evaluate example conversations before claiming response quality.

These are improvement directions, not claims of features already implemented.
The hosted deployment was not independently tested for this profile.

[Back to profile](../../README.md)
