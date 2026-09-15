"""FastAPI application exposing graph resumption after human review."""

from typing import Any

from fastapi import FastAPI
from langgraph.types import Command

from mail_agent.graph import compile_graph

app = FastAPI(title="Mail Agent")
graph = compile_graph()


@app.post("/runs/{thread_id}/resume")
async def resume_run(thread_id: str, decision: dict[str, Any]) -> dict[str, Any]:
    """Resume an interrupted graph run with a human decision payload."""

    result = await graph.ainvoke(
        Command(resume=decision),
        config={"configurable": {"thread_id": thread_id}},
    )
    return result