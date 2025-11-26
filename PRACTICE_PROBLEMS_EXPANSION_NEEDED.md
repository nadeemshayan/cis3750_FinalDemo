# Practice Problems - Expansion Required

## Current Status
The practice problem bank currently has **limited questions per topic**:
- basic_derivatives: 7 problems
- product_quotient: 3 problems
- chain_rule: 3 problems
- applications: 5 problems
- implicit_differentiation: 5 problems
- trigonometric: 5 problems  
- exponential_log: 5 problems

**Total: ~33 problems across 7 categories**

## Target Goal
**20+ problems per topic** for comprehensive practice

## Expansion Plan

### 1. Basic Derivatives (Target: 20 problems)
**Need: 13 more problems**

Add problems covering:
- Power rule with negative exponents
- Power rule with fractional exponents
- Combinations of polynomial terms
- Constants and linear functions
- Square roots and cube roots rewritten as powers

### 2. Product/Quotient Rules (Target: 20 problems)
**Need: 17 more problems**

Add problems covering:
- Simple product rule: polynomial × polynomial
- Product rule: polynomial × trig
- Product rule: exponential × polynomial
- Product rule: three functions
- Quotient rule: polynomial over polynomial
- Quotient rule: trig over polynomial
- Quotient rule: combined with power rule

### 3. Chain Rule (Target: 20 problems)
**Need: 17 more problems**

Add problems covering:
- Composition of polynomials
- Trig functions of polynomials
- Exponentials of polynomials
- Powers of trig functions
- Nested compositions (chain rule twice)
- Square roots of functions
- Multiple chain rule applications

### 4. Applications (Target: 20 problems)
**Need: 15 more problems**

Add problems covering:
- More velocity/acceleration problems
- Optimization problems (max/min)
- Related rates (various scenarios)
- Marginal cost/revenue
- Population growth models
- Area and volume rate problems
- Critical points and inflection points

### 5. Implicit Differentiation (Target: 20 problems)
**Need: 15 more problems**

Add problems covering:
- Circles and ellipses
- Hyperbolas
- Trig implicit equations
- Exponential implicit equations
- Second derivatives implicitly
- Tangent lines to implicit curves

### 6. Trigonometric Derivatives (Target: 20 problems)
**Need: 15 more problems**

Add problems covering:
- All six trig functions
- Inverse trig functions
- Trig + chain rule combinations
- Products of trig functions
- Quotients of trig functions
- Trig identities in derivatives

### 7. Exponential/Logarithmic (Target: 20 problems)
**Need: 15 more problems**

Add problems covering:
- Natural exponential with chain rule
- Natural log with chain rule
- Logarithmic differentiation
- Base other than e (log_a)
- Exponential growth/decay
- Log properties in derivatives

## Implementation Notes

### Problem Structure
Each problem must have:
```python
{
    "id": "unique_id",
    "question": "Clear problem statement",
    "options": ["Answer 1", "Answer 2", "Answer 3", "Answer 4"],
    "correct": 0,  # index of correct answer
    "explanation": "Detailed step-by-step solution",
    "topic": "Topic name",
    "difficulty": "easy" | "medium" | "hard"
}
```

### Difficulty Distribution
For each topic with 20 problems:
- **Easy**: 8 problems (40%)
- **Medium**: 8 problems (40%)
- **Hard**: 4 problems (20%)

### Quality Standards
- Clear, unambiguous wording
- Four plausible answer choices
- Detailed explanations showing work
- Progressive difficulty within each topic
- Cover breadth of applications

## Quick Addition Template

```python
{
    "id": "bd8",
    "question": "Find the derivative of f(x) = 4x³ - 2x + 5",
    "options": ["12x² - 2", "12x² + 2", "12x³ - 2", "4x² - 2"],
    "correct": 0,
    "explanation": "Apply power rule to each term: d/dx(4x³) = 12x², d/dx(-2x) = -2, d/dx(5) = 0. Result: 12x² - 2",
    "topic": "Power Rule",
    "difficulty": "easy"
},
```

## Priority Order

1. **Basic Derivatives** (most fundamental, needed first)
2. **Chain Rule** (most commonly used advanced rule)
3. **Product/Quotient Rules** (essential for complex functions)
4. **Applications** (real-world relevance)
5. **Trigonometric** (specific function type)
6. **Exponential/Log** (specific function type)
7. **Implicit Differentiation** (advanced technique)

## Testing After Expansion

After adding problems, verify:
- ✅ All problem IDs are unique
- ✅ All correct answers are valid indices
- ✅ Explanations are clear and accurate
- ✅ Difficulty ratings are appropriate
- ✅ Topics map correctly to ML system
- ✅ No duplicate questions
- ✅ Balanced difficulty distribution

## Integration with ML

The expanded problem bank will improve:
- **Spaced Repetition**: More problems to rotate through
- **Adaptive Difficulty**: Better selection of easy/medium/hard
- **Topic Targeting**: Deeper practice in weak areas
- **Learning Velocity**: More data points for ML calculations
- **Confidence Scores**: More accurate topic mastery assessment

## File Location
`/pages/practice_problems.py` - lines 12-340 (PRACTICE_PROBLEMS dictionary)

## Estimated Time
- ~2-3 hours to write 100+ new problems with quality explanations
- Can be done incrementally, topic by topic
