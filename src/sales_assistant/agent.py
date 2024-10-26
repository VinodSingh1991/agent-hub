from langchain_core.runnables import Runnable, RunnableConfig
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)
            if (
                result.tool_calls
                or result.content
                and (
                    not isinstance(result.content, list)
                    or result.content[0].get("text")
                )
            ):
                break
            messages = state["messages"] + [("user", "Respond with a real output.")]
            state = {**state, "messages": messages}
        return {"messages": result}
