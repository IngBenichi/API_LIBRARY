Here is the Markdown documentation for the provided FastAPI code in English:


# FastAPI Application for AHP Calculations

This FastAPI application provides endpoints for calculating the Analytic Hierarchy Process (AHP) using various methods including standard AHP, fuzzy AHP, and pairwise comparison fuzzy AHP.

## Required Libraries

Make sure to install the following libraries before running the application:

```bash
pip install -r requirements.txt
```

## Application Setup

The application is initialized with CORS middleware to allow cross-origin requests.

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from pyDecision.algorithm import ahp_method, fuzzy_ahp_method, ppf_ahp_method

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Static Dataset for AHP

The application defines a static dataset for AHP calculations:

```python
dataset1 = np.array([
    [1, 1/3, 1/5, 1, 1/4, 1/2, 3],
    [3, 1, 1/2, 2, 1/3, 3, 3],
    [5, 2, 1, 4, 5, 6, 5],
    [1, 1/2, 1/4, 1, 1/4, 1, 2],
    [4, 3, 1/5, 4, 1, 3, 2],
    [2, 1/3, 1/6, 1, 1/3, 1, 1/3],
    [1/3, 1/3, 1/5, 1/2, 1/2, 3, 1]
])
```

## AHP Request Model

The `AHPRequest` model defines the structure for incoming requests, specifying the weight derivation method.

```python
class AHPRequest(BaseModel):
    weight_derivation: str = 'geometric'  # Options: 'mean', 'geometric', 'max_eigen'
```

## AHP Calculation Endpoint

The `/calculate-ahp/` endpoint processes AHP calculations based on the provided dataset.

### Request Example

```json
{
    "weight_derivation": "geometric"
}
```

### Response Example

```json
{
    "weights": [0.123, 0.234, 0.345, 0.456, 0.567, 0.678, 0.789],
    "consistency_ratio": 0.05,
    "consistency_message": "The solution is consistent",
    "dataset1": [[1, 0.33, 0.2, 1, 0.25, 0.5, 3], ...]
}
```

### Error Handling

If the weight derivation option is invalid or an error occurs during calculations, appropriate HTTP exceptions will be raised.

## Fuzzy AHP Calculation

The application also includes an endpoint for fuzzy AHP calculations using a fixed dataset.

### Static Dataset for Fuzzy AHP

```python
dataset2 = [
    [(1, 1, 1), (4, 5, 6), (3, 4, 5), (6, 7, 8)],
    [(1/6, 1/5, 1/4), (1, 1, 1), (1/3, 1/2, 1), (2, 3, 4)],
    [(1/5, 1/4, 1/3), (1, 2, 3), (1, 1, 1), (2, 3, 4)],
    [(1/8, 1/7, 1/6), (1/4, 1/3, 1/2), (1/4, 1/3, 1/2), (1, 1, 1)]
]
```

### Fuzzy AHP Endpoint

The `/fuzzy-ahp` endpoint processes fuzzy AHP calculations.

### Response Example

```json
{
    "dataset2": [[(1, 1, 1), ...], ...],
    "fuzzy_weights": [[0.123, 0.234, 0.345], ...],
    "crisp_weigths": [0.456, 0.567, 0.678],
    "normalized_weights": [0.789, 0.890, 0.901],
    "consistency_ratio": 0.05,
    "consistency_message": "The solution is consistent"
}
```

## Pairwise Comparison Fuzzy AHP Calculation

The application also includes an endpoint for pairwise comparison fuzzy AHP calculations.

### Static Dataset for PPF AHP

```python
dataset3 = [
    [(0, 0), (3, 1), (1, 4), (1, 3), (1, 3), (4, 2)],
    [(1, 3), (0, 0), (1, 6), (2, 5), (2, 5), (0, 2)],
    [(4, 1), (6, 1), (0, 0), (2, 1), (3, 1), (5, 1)],
    [(3, 1), (5, 2), (1, 2), (0, 0), (2, 1), (7, 2)],
    [(3, 1), (5, 2), (1, 3), (1, 2), (0, 0), (4, 2)],
    [(2, 4), (2, 0), (1, 5), (2, 7), (2, 4), (0, 0)]
]
```

### PPF AHP Endpoint

The `/ppf-ahp` endpoint processes pairwise comparison fuzzy AHP calculations.

### Response Example

```json
{
    "weights": [0.1, 0.2, 0.3, 0.15, 0.25],
    "consistency_ratio": 0.05,
    "is_consistent": true,
    "dataset3": [[(0, 0), (3, 1), ...], ...],
    "consistency_message": "The solution is consistent."
}
```

## Running the Application

To run the application, save the code in a file (e.g., `main.py`) and execute:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## Documentation

You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.
```

Summary of the Markdown Content:

1. Project Overview: Introduction to the FastAPI application for AHP calculations.
2. Setup Instructions: Details on required libraries and installation.
3. Code Structure: Explanation of the setup, including middleware and datasets.
4. Endpoints: Detailed documentation for each endpoint including request and response examples.
5. Error Handling: Notes on how errors are managed.
6. Running Instructions: Instructions for running the application and accessing the API documentation.

Feel free to adjust any specific sections or details as needed!
