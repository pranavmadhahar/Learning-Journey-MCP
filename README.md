# Learning-Journey-MCP

This repository is part of my **Learning Journey series**, documenting my exploration of the **Model Context Protocol (MCP)** and AI-to-tool integration.

Here, I explore MCP fundamentals, build MCP servers with **FastMCP**, connect them with **LangChain**, and experiment with tools, resources, clients, transports, and MCP-based application architecture.

## Note

This repository documents my **hands-on learning and experimentation with MCP**.

The projects are intentionally kept small and focused so that each implementation reinforces a specific MCP concept, while maintaining clean repository structure, documentation, and Git history.

## Contents

* MCP architecture and core concepts
* Tools, resources, and prompts
* JSON-RPC 2.0
* MCP transports
* MCP server development with FastMCP
* Local MCP servers using stdio
* Expense Tracker MCP server
* Math MCP server
* MCP clients with LangChain
* Connecting multiple MCP servers through a client
* MCP client/server configuration
* MCP learning notes and experiments

## Projects

### Expense Tracker MCP Server

A local MCP server built with **FastMCP** that provides tools for managing expenses, credits, categories, and spending summaries using SQLite.

### Math MCP Server

A simple MCP server exposing mathematical operations as MCP tools, including input validation and numeric conversion.

### LangChain MCP Client

A client implementation using **LangChain's MCP integration** to connect an AI application with MCP servers and consume their exposed capabilities.

## Goals

* Understand the architecture and purpose of MCP
* Learn how AI applications interact with external tools and services
* Build MCP servers using FastMCP
* Understand MCP clients and server communication
* Integrate MCP with LangChain
* Experiment with tools, resources, prompts, and transports
* Develop practical understanding through small, focused projects
* Maintain professional repository hygiene and meaningful Git history

---

*Part of the Learning-Journey series: HTML-CSS → Tailwind-Bootstrap → React → Flask → Django → MongoDB → Agentic AI → MCP.*
