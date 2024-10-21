from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from pyDecision.algorithm import ahp_method,fuzzy_ahp_method,ppf_ahp_method
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definir el dataset1 estático
dataset1 = np.array([
    # g1     g2     g3     g4     g5     g6     g7                  
    [1,     1/3,   1/5,   1,     1/4,   1/2,   3],   # g1
    [3,     1,     1/2,   2,     1/3,   3,     3],   # g2
    [5,     2,     1,     4,     5,     6,     5],   # g3
    [1,     1/2,   1/4,   1,     1/4,   1,     2],   # g4
    [4,     3,     1/5,   4,     1,     3,     2],   # g5
    [2,     1/3,   1/6,   1,     1/3,   1,     1/3], # g6
    [1/3,   1/3,   1/5,   1/2,   1/2,   3,     1]    # g7
])

# Modelo de datos de entrada
class AHPRequest(BaseModel):
    weight_derivation: str = 'geometric'  # Opciones: 'mean', 'geometric', 'max_eigen'


@app.post("/calculate-ahp/")
def PPF_AHP(request: AHPRequest):
    
    if request.weight_derivation not in ['mean', 'geometric', 'max_eigen']:
        raise HTTPException(status_code=400, detail="Opción de derivación de peso no válida. Use 'mean', 'geometric' o 'max_eigen'.")

    
    try:
        weights, rc = ahp_method(dataset1, wd=request.weight_derivation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    weights_rounded = [round(w, 3) for w in weights]
    rc_rounded = round(rc, 2)
    consistency_message = "The solution is consistent" if rc <= 0.10 else "The solution is inconsistent, the pairwise comparisons must be reviewed"

    
    dataset_list = dataset1.tolist()

    
    return {
        "weights": weights_rounded,
        "consistency_ratio": rc_rounded,
        "consistency_message": consistency_message,
        "dataset1": dataset_list
    }





# Dataset fijo
dataset2 = [
    [(1, 1, 1), (4, 5, 6), (3, 4, 5), (6, 7, 8)],   # g1
    [(1/6, 1/5, 1/4), (1, 1, 1), (1/3, 1/2, 1), (2, 3, 4)],   # g2
    [(1/5, 1/4, 1/3), (1, 2, 3), (1, 1, 1), (2, 3, 4)],   # g3
    [(1/8, 1/7, 1/6), (1/4, 1/3, 1/2), (1/4, 1/3, 1/2), (1, 1, 1)]    # g4
]

@app.get("/fuzzy-ahp")

def calculate_fuzzy_ahp():
    try:
        
        fuzzy_weights, crisp_weigths, normalized_weights, rc = fuzzy_ahp_method(dataset2)

        
        result = {
            "dataset2": dataset2,
            "fuzzy_weights": [list(np.around(weight, 3)) for weight in fuzzy_weights],
            "crisp_weigths": [round(weight, 3) for weight in crisp_weigths],
            "normalized_weights": [round(weight, 3) for weight in normalized_weights],
            "consistency_ratio": round(rc, 2),
            "consistency_message": "The solution is consistent" if rc <= 0.10 else "The solution is inconsistent, the pairwise comparisons must be reviewed"
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")
    


dataset3 = [
    [(0, 0), (3, 1), (1, 4), (1, 3), (1, 3), (4, 2)],
    [(1, 3), (0, 0), (1, 6), (2, 5), (2, 5), (0, 2)],
    [(4, 1), (6, 1), (0, 0), (2, 1), (3, 1), (5, 1)],
    [(3, 1), (5, 2), (1, 2), (0, 0), (2, 1), (7, 2)],
    [(3, 1), (5, 2), (1, 3), (1, 2), (0, 0), (4, 2)],
    [(2, 4), (2, 0), (1, 5), (2, 7), (2, 4), (0, 0)]
]

class AHPResponse(BaseModel):
    weights: list
    consistency_ratio: float
    is_consistent: bool
    dataset3: list
    consistency_message: str  

@app.get("/ppf-ahp", response_model=AHPResponse)
async def ppf_ahp():
    # Call PPF AHP Function
    weights, rc = ppf_ahp_method(dataset3)

    
    weights_list = [round(w, 5) for w in weights]
    is_consistent = rc <= 0.10

    
    if is_consistent:
        consistency_message = "The solution is consistent."
    else:
        consistency_message = "The solution is inconsistent; the pairwise comparisons must be reviewed."

    return AHPResponse(
        weights=weights_list,
        consistency_ratio=round(rc, 4),
        is_consistent=is_consistent,
        dataset3=dataset3,
        consistency_message=consistency_message
    )

