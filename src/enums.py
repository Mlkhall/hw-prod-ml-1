from enum import StrEnum


class QueuesNames(StrEnum):
    target_queue = "y_true"
    predictions_queue = "y_pred"
    features_queue = "features"
