from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from pyDecision.algorithm import ahp_method
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definir el dataset estático
STATIC_DATASET = np.array([
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
def calculate_ahp(request: AHPRequest):
    
    if request.weight_derivation not in ['mean', 'geometric', 'max_eigen']:
        raise HTTPException(status_code=400, detail="Opción de derivación de peso no válida. Use 'mean', 'geometric' o 'max_eigen'.")

    
    try:
        weights, rc = ahp_method(STATIC_DATASET, wd=request.weight_derivation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    weights_rounded = [round(w, 3) for w in weights]
    rc_rounded = round(rc, 2)
    consistency_message = "The solution is consistent" if rc <= 0.10 else "The solution is inconsistent, the pairwise comparisons must be reviewed"

    
    dataset_list = STATIC_DATASET.tolist()

    
    return {
        "weights": weights_rounded,
        "consistency_ratio": rc_rounded,
        "consistency_message": consistency_message,
        "dataset": dataset_list
    }