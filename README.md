Here's the revised Markdown documentation that includes a section about the fuzzy AHP method:

```markdown
# FastAPI Application for AHP Calculation

This code creates a FastAPI-based web application that calculates the Analytic Hierarchy Process (AHP) using predefined datasets and the `pyDecision` library. The app is designed to be a simple API for calculating AHP with different weight derivation methods.

## Key Components

1. **Libraries and Dependencies:**
   - `FastAPI`: A Python web framework for building APIs.
   - `HTTPException`: Used to handle HTTP exceptions.
   - `BaseModel` from `pydantic`: Used to define data models.
   - `numpy`: For numerical operations.
   - `pyDecision.algorithm.ahp_method`: The AHP algorithm from the `pyDecision` library.
   - `CORSMiddleware`: For enabling Cross-Origin Resource Sharing.

2. **CORS Configuration:**
   The application allows all origins, methods, and headers to access the API, making it accessible from any domain.

3. **Static Dataset:**
   A pairwise comparison matrix (`STATIC_DATASET`) is defined as a NumPy array, representing criteria weights for the AHP calculation. 

   ```python
   STATIC_DATASET = np.array([
       [1,     1/3,   1/5,   1,     1/4,   1/2,   3],   # g1
       [3,     1,     1/2,   2,     1/3,   3,     3],   # g2
       [5,     2,     1,     4,     5,     6,     5],   # g3
       [1,     1/2,   1/4,   1,     1/4,   1,     2],   # g4
       [4,     3,     1/5,   4,     1,     3,     2],   # g5
       [2,     1/3,   1/6,   1,     1/3,   1,     1/3], # g6
       [1/3,   1/3,   1/5,   1/2,   1/2,   3,     1]    # g7
   ])
   ```

4. **Input Data Model:**
   An input model `AHPRequest` is defined, using `BaseModel` from `pydantic`. It contains:
   - `weight_derivation`: Specifies the method for deriving weights, with options: `'mean'`, `'geometric'`, or `'max_eigen'`. The default is `'geometric'`.

5. **API Endpoint:**
   The endpoint `/calculate-ahp/` is defined to perform the AHP calculation:
   - It accepts a POST request with a JSON payload matching the `AHPRequest` model.
   - Validates the `weight_derivation` input, ensuring it is one of the allowed values.
   - Calculates weights and consistency ratio using the AHP method from the `pyDecision` library.
   - Rounds the weights and consistency ratio to three and two decimal places, respectively.
   - Provides a message indicating whether the solution is consistent based on the consistency ratio (`rc`).
   - Converts the static dataset to a list for easy JSON serialization in the response.

## Endpoint: `/calculate-ahp/`

- **Method**: POST
- **Request Body**:
  ```json
  {
    "weight_derivation": "geometric"
  }
  ```
- **Response**:
  - Returns a JSON object with the following fields:
    - `"weights"`: A list of rounded weight values.
    - `"consistency_ratio"`: The rounded consistency ratio.
    - `"consistency_message"`: A message indicating whether the solution is consistent.
    - `"dataset"`: The original dataset in list format.

## Example Response

```json
{
  "weights": [0.113, 0.226, 0.345, 0.087, 0.146, 0.044, 0.038],
  "consistency_ratio": 0.05,
  "consistency_message": "The solution is consistent",
  "dataset": [
    [1, 0.333, 0.2, 1, 0.25, 0.5, 3],
    [3, 1, 0.5, 2, 0.333, 3, 3],
    [5, 2, 1, 4, 5, 6, 5],
    [1, 0.5, 0.25, 1, 0.25, 1, 2],
    [4, 3, 0.2, 4, 1, 3, 2],
    [2, 0.333, 0.167, 1, 0.333, 1, 0.333],
    [0.333, 0.333, 0.2, 0.5, 0.5, 3, 1]
  ]
}
```

6. **Fuzzy AHP Method:**
   The fuzzy AHP method allows for more nuanced comparisons by using fuzzy numbers to represent uncertainties in judgments. This method is particularly useful when exact values are difficult to determine, enabling decision-makers to express their preferences in a range rather than as precise numbers. 

   In this application, a second dataset is used for fuzzy AHP calculations, which consists of fuzzy pairwise comparisons.

   ```python
   dataset = [
       [(1, 1, 1), (4, 5, 6), (3, 4, 5), (6, 7, 8)],   # g1
       [(1/6, 1/5, 1/4), (1, 1, 1), (1/3, 1/2, 1), (2, 3, 4)],   # g2
       [(1/5, 1/4, 1/3), (1, 2, 3), (1, 1, 1), (2, 3, 4)],   # g3
       [(1/8, 1/7, 1/6), (1/4, 1/3, 1/2), (1/4, 1/3, 1/2), (1, 1, 1)]    # g4
   ]
   ```

## Endpoint: `/fuzzy-ahp`

- **Method**: GET
- **Response**:
  - Returns a JSON object with the following fields:
    - `"dataset"`: The dataset used for calculations.
    - `"fuzzy_weights"`: Fuzzy weights rounded to three decimal places.
    - `"crisp_weights"`: Crisp weights rounded to three decimal places.
    - `"normalized_weights"`: Normalized weights rounded to three decimal places.
    - `"consistency_ratio"`: The consistency ratio rounded to two decimal places.
    - `"consistency_message"`: A message indicating whether the solution is consistent.

## Example Response for Fuzzy AHP

```json
{
  "dataset": [
    [(1, 1, 1), (4, 5, 6), (3, 4, 5), (6, 7, 8)],
    [(1/6, 1/5, 1/4), (1, 1, 1), (1/3, 1/2, 1), (2, 3, 4)],
    [(1/5, 1/4, 1/3), (1, 2, 3), (1, 1, 1), (2, 3, 4)],
    [(1/8, 1/7, 1/6), (1/4, 1/3, 1/2), (1/4, 1/3, 1/2), (1, 1, 1)]
  ],
  "fuzzy_weights": [[0.2, 0.3, 0.5], [0.1, 0.2, 0.7]],
  "crisp_weights": [0.15, 0.25, 0.45, 0.15],
  "normalized_weights": [0.15, 0.25, 0.45, 0.15],
  "consistency_ratio": 0.08,
  "consistency_message": "The solution is consistent"
}
```

This application provides a straightforward way to perform AHP calculations using predefined pairwise comparison matrices, making it useful for decision-making scenarios.
```

Feel free to make any additional changes or let me know if you need further adjustments!
