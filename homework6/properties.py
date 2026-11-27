PROPERTIES_ADD_SCALAR = '''
Свойства операций сложения матриц и умножения на число:

∀ A, B, C ∈ W_m×n(R), ∀ α, β ∈ R:
1) A + B = B + A
2) (A + B) + C = A + (B + C)
3) ∃ O ∈ W_m×n(R) : A + O = A
4) ∀ A ∃ (-A) ∈ W_m×n(R) : A + (-A) = O
5) α(A + B) = αA + αB
6) (α + β)A = αA + βA
7) α(βA) = (αβ)A
8) 1 · A = A
'''

PROPERTIES_MULTIPLICATION = '''
Свойства операции умножения матриц:

1. AB ≠ BA (произведение матриц не коммутативно).
2. A(BC) = (AB)C, для ∀ A ∈ W_m×n(R), B ∈ W_n×k(R), C ∈ W_k×s(R).
3.1. (A+B)C = AC + BC, для ∀ A, B ∈ W_m×n(R), C ∈ W_n×k(R).
3.2. D(A+B) = DA + DB, для ∀ A, B ∈ W_m×n(R), D ∈ W_k×m(R).
4. AO = OA = O, для ∀ A, O ∈ W_n×n(R).
5. AE = EA = A, для ∀ A, E ∈ W_n×n(R).
6. α(AB) = (αA)B = A(αB), для ∀ A ∈ W_m×n(R), B ∈ W_n×k(R).
'''

PROPERTIES_INVERSE = '''
Свойства обратной матрицы:

1) (A⁻¹)⁻¹ = A
2) (A · B)⁻¹ = B⁻¹ · A⁻¹
3) (Aᵗ)⁻¹ = (A⁻¹)ᵗ
4) det A · det A⁻¹ = 1
'''
