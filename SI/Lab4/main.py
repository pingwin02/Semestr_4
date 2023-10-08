import numpy as np

from decision_tree import DecisionTree
from random_forest import RandomForest
from sklearn.tree import DecisionTreeClassifier
from load_data import generate_data, load_titanic


def main():
    np.random.seed(123)

    train_data, test_data = load_titanic()

    print("Decision Tree: ")

    dt = DecisionTree({"depth": 14})
    dt.train(*train_data)
    dt.evaluate(*train_data)
    dt.evaluate(*test_data)

    print("Random Forest: ")

    rf = RandomForest({"ntrees": 75, "feature_subset": 3, "depth": 14})
    rf.train(*train_data)
    rf.evaluate(*train_data)
    rf.evaluate(*test_data)

    print("Sklearn: ")

    dc = DecisionTreeClassifier()
    dc.fit(*train_data)
    print(f"Accuracy: {round(dc.score(*train_data), 2)}")
    print(f"Accuracy: {round(dc.score(*test_data), 2)}")


if __name__ == "__main__":
    main()
