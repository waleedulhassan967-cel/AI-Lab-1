# Lab 6: NLP Fundamentals - Tokenization, Embeddings & Text Chunking

This folder contains the complete, executable solution for **Lab 6 (CA1601400 - Artificial Intelligence Lab)**.

## Project Structure
- `lab6_search.py`: Core `Retriever` class supporting TF-IDF and Sentence Transformer backends.
- `task1_tokens.py`: Script comparing Whitespace, Regex, and Subword tokenization across edge-case strings.
- `guided_chatbot.py` & `task1_chatbot_check.py`: Confirmation-based FAQ chatbot implementation and assertions.
- `task2_chunks.py`: Text chunking algorithms (Word-windows & Sentence-aware splitting) with unit tests.
- `create_dataset.py`: Script to generate `corpus.json` and `queries.json` datasets.
- `task3_retrieval.py`: Pipeline evaluation script generating `retrieval_log.csv` (Hit@3 & MRR@3 metrics).
- `document_chatbot.py`: Interactive traceable document retrieval chatbot interface.

## Setup Instructions

1. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv .venv
   # On Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source .venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execution Steps**:
   ```bash
   # Run Task 1 Tokenization Analysis
   python task1_tokens.py

   # Test FAQ Chatbot
   python task1_chatbot_check.py

   # Run Task 2 Chunking Unit Tests
   python task2_chunks.py

   # Generate Datasets
   python create_dataset.py

   # Run Task 3 Retrieval Evaluation Pipeline
   python task3_retrieval.py

   # Launch Interactive Document Chatbot
   python document_chatbot.py
   ```
