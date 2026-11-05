# Spades Trick Predictor

Can you predict how many tricks a Spades hand will win just from the cards dealt? This project simulates 100,000 rounds of Spades to build its own dataset, then trains regression and machine learning models to predict tricks won per player per round.

This was my final project for Data Mining at Hunter College (CUNY), December 2024.

## The problem

In Spades, each team bids the number of tricks (books) it expects to win, and it scores only if it makes the bid. A good bid depends on reading the strength of your hand. Spades are always trump, so they beat any other suit. No public dataset of hands and outcomes existed, so I generated one.

## Approach

**1. Simulation** (`Spades Game.py`)
An object-oriented simulator with `Player` and `Spades_Game` classes deals cards and plays 100,000 rounds among four players. Players pick a random legal card each trick: they follow the leading suit when they can and play any card when they can't. The simulator records:
- each player's starting hand per round
- the cards played and the winning card in every trick
- tricks won by each player per round

To keep the focus on hand strength, the simulation skips bags, scoring, and the rule against leading with spades.

**2. Exploratory analysis and regression diagnostics** (`Spades Analysis.ipynb`)
- Calculated how often each card wins when played. As expected, spades and high face cards dominate.
- Checked linear regression assumptions:
  - correlation of each card with tricks won
  - variance inflation factors for multicollinearity (all near 1)
  - Q-Q plots and residual histograms for normality
  - the Durbin-Watson statistic for autocorrelation
- Engineered features: cards held in each suit, number of face cards, and squared, cubed, and log transforms to capture non-linear effects.

**3. Modeling**
Compared models using an 80/20 train/test split and 4-fold grid-search cross-validation in scikit-learn:

| Model | Notes |
| --- | --- |
| Linear regression | Baseline; explained about half the variation in tricks won |
| Ridge regression | Tuned the regularization strength (best α = 100); no improvement over linear |
| Random forest | Tuned the number of trees; 100 estimators performed best |

## Results

- The random forest predicted tricks won within about **one trick on average (MAE 0.94)**.
- R² was 0.91 on training data and 0.49 on test data. The model fits the data it has seen well but generalizes less well, which is expected given how random simulated play is.
- A bid equal to the model's prediction was made **68% of the time**.
- Feature importance showed that **the number of face cards and the number of spades** drive outcomes most.

## Limitations and next steps

Random play captures how strong each card is, but not real strategy like cutting, signaling a partner, or underbidding with a lead. Training on hands from experienced players would likely improve how well the model generalizes.

## Running the project

Requires Python 3 with NumPy, pandas, Matplotlib, seaborn, scikit-learn, and statsmodels:

```
pip install numpy pandas matplotlib seaborn scikit-learn statsmodels
```

1. Run `Spades Game.py` to simulate the games. It writes three CSV files: `cards_played_per_trick.csv`, `tricks_won_by_player.csv`, and `player_hands_by_round.csv`. Update the output paths at the bottom of the script to a folder on your machine.
2. Open `Spades Analysis.ipynb`, point the file paths at those CSVs, and run the cells.

The full write-up is in `Brian Holliday Final Project Write Up.docx`.
