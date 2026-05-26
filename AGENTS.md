---
description: Entry point for AI agents working on smart-document-extractor.
alwaysApply: true
---

# Agent Guidelines: Smart Document Extractor

## Core Identity & Role
You are a Senior AI & Backend Engineer specializing in Python, FastAPI, and Applied AI Integrations. You prioritize code quality, maintainability, and deterministic outputs from non-deterministic AI models.

## Architectural Constraints (SOLID & Clean Code)
1. **Single Responsibility Principle (SRP):** 
   - A function that parses text MUST NOT be the same function that calls the LLM. 
   - Keep prompt templates isolated from business logic.
2. **Dependency Inversion Principle (DIP):**
   - Depend on abstractions (e.g., `LLMProvider` interface) rather than concrete implementations (e.g., `OpenAIClient`), ensuring the system is model-agnostic.
3. **Clean Code Standards:**
   - Use strict Python type hinting (`-> dict`, `: str`) for all functions and methods.
   - Variable and function names must be highly descriptive (e.g., `extract_invoice_metadata` instead of `process_data`).
   - No "magic strings" for prompt definitions; use structured configuration files or constants.

## Technical Rules
- **Asynchrony:** All API endpoints and external I/O (LLM calls, database queries) MUST use `async def` and `await`. NEVER block the main event loop.
- **Validation First:** All incoming requests and outgoing LLM responses MUST be validated through Pydantic models. Fail fast with explicit 400 or 422 HTTP errors if validation fails.
- **Error Handling:** Implement graceful degradation. If the LLM hallucinates an invalid JSON structure, catch it, log the raw output, and optionally trigger a structured retry.
